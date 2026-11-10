#!/usr/bin/env python3
"""Assistant-written bounded checks; not full course training or learner trial."""
from pathlib import Path
import ast, contextlib, dataclasses, io, json, os, sys
import torch
import torch.nn as nn
import torch.nn.functional as F
B=Path(__file__).resolve().parent
report={'torch':torch.__version__,'device':'cpu','scope':'bounded mathematical and structural checks; not full training','checks':{}}
torch.manual_seed(1337);torch.set_num_threads(2)
sys.path[:0]=[str(B/'micrograd'),str(B/'minbpe')]
from micrograd.engine import Value
a=Value(3.0);b=a+a;b.backward();assert a.grad==2
report['checks']['micrograd_repeated_node']={'gradient':a.grad,'status':'passed'}
# Execute the author's notebook exercise cells, removing notebook-only magic.
p=B/'nn-zero-to-hero/lectures/makemore/makemore_part4_backprop.ipynb'
cells=json.loads(p.read_text())['cells'];scope={};grad_checks=[]
def cmp(s,dt,t):
 diff=float((dt-t.grad).abs().max());ok=bool(torch.allclose(dt,t.grad,atol=1e-6,rtol=1e-4))
 grad_checks.append({'tensor':s,'maxdiff':diff,'within_atol_1e-6_rtol_1e-4':ok});assert ok,(s,diff)
oldcwd=Path.cwd()
try:
 os.chdir(p.parent)
 with contextlib.redirect_stdout(io.StringIO()):
  for k in [2,3,4,5,7,8,9,10,11,12,13,19,20]:
   c=''.join(cells[k]['source']);c='\n'.join(l for l in c.splitlines() if not l.startswith('%'))
   exec(compile(c,str(p)+f':cell{k}','exec'),scope)
   if k==7:scope['cmp']=cmp
finally:os.chdir(oldcwd)
report['checks']['manual_backprop']={'status':'passed','items':grad_checks}
from minbpe import BasicTokenizer
t=BasicTokenizer();t.train('aaabdaaabac',259);ids=t.encode('aaabdaaabac');assert ids==[258,100,258,97,99]
roundtrips=['','hello','中文测试','안녕하세요 😉','aaaaaaa']
for s in roundtrips:assert t.decode(t.encode(s))==s
report['checks']['bpe']={'status':'passed','ids':ids,'roundtrips':roundtrips}
# Extract only class declarations: importing train_gpt2.py itself would start a large run.
source=B/'build-nanogpt/train_gpt2.py';tree=ast.parse(source.read_text())
classes=[n for n in tree.body if isinstance(n,ast.ClassDef) and n.name in ['CausalSelfAttention','MLP','Block','GPTConfig','GPT']]
scope={'torch':torch,'nn':nn,'F':F,'dataclass':dataclasses.dataclass,'__name__':'bounded_gpt2_check'}
exec(compile(ast.Module(body=classes,type_ignores=[]),str(source),'exec'),scope)
m=scope['GPT'](scope['GPTConfig'](block_size=8,vocab_size=32,n_layer=2,n_head=2,n_embd=32));m.eval()
x=torch.randint(0,32,(2,8));y=torch.randint(0,32,(2,8));logits,loss=m(x,y)
assert logits.shape==(2,8,32)
x2=x.clone();x2[:,4:]=(x2[:,4:]+1)%32
with torch.no_grad():causal_diff=float((m(x)[0][:,:4]-m(x2)[0][:,:4]).abs().max())
assert causal_diff<1e-6
assert m.transformer.wte.weight is m.lm_head.weight
opt=torch.optim.AdamW(m.parameters(),lr=0.01);losses=[]
for _ in range(10):
 opt.zero_grad();_,loss=m(x,y);losses.append(float(loss.detach()));loss.backward();opt.step()
assert losses[-1]<losses[0]
report['checks']['gpt2_tiny']={'status':'passed','shape':list(logits.shape),'causal_diff':causal_diff,'weight_tied':True,'losses':losses,'parameters':sum(p.numel() for p in m.parameters()),'note':'2-layer 32-wide random model, 10 updates, not 124M training'}
print(json.dumps(report,ensure_ascii=False,indent=2))
