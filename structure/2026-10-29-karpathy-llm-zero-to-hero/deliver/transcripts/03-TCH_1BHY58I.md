# 原始逐字稿 03：Building makemore Part 2: MLP

> 来源：https://www.youtube.com/watch?v=TCH_1BHY58I
> 语言：英文；YouTube 自动字幕，非人工逐字校对。仅重排空行与排版，保留非空事件顺序及措辞；不翻译、不修正识别错误。时间戳来自 JSON3。
> 视频时长：01:15:39；字幕末尾起始时间：01:15:37。

[00:00:00] Hi everyone.
[00:00:02] Today we are continuing our
[00:00:03] implementation of makemore.
[00:00:05] Now in the last lecture we implemented
[00:00:06] the bigram language model and we
[00:00:08] implemented both using counts and also
[00:00:11] using a super simple neural network that
[00:00:13] had a single linear layer.
[00:00:15] Now this is the
[00:00:17] Jupyter notebook that we built out last
[00:00:19] lecture.
[00:00:20] And we saw that the way we approached
[00:00:21] this is that we looked at only the
[00:00:23] single previous character and we
[00:00:25] predicted the distribution for the
[00:00:26] character that would go next in the
[00:00:28] sequence. And we did that by taking
[00:00:30] counts and normalizing them into
[00:00:32] probabilities
[00:00:33] so that each row here sums to one.
[00:00:36] Now this is all well and good if you
[00:00:38] only have one character of previous
[00:00:40] context.
[00:00:41] And this works and it's approachable.
[00:00:43] The problem with this model of course is
[00:00:45] that the predictions from this model are
[00:00:48] not very good because you only take one
[00:00:50] character of context. So the model
[00:00:52] didn't produce very name-like sounding
[00:00:54] things.
[00:00:56] Now the problem with this approach
[00:00:57] though is that if we are to take more
[00:01:00] context into account when predicting the
[00:01:01] next character in the sequence, things
[00:01:03] quickly blow up and this table the size
[00:01:06] of this table grows and in fact it grows
[00:01:08] exponentially with the length of the
[00:01:10] context.
[00:01:11] Because if we only take a single
[00:01:12] character at a time, that's 27
[00:01:13] possibilities of context.
[00:01:16] But if we take two characters in the
[00:01:17] past and try to predict the third one,
[00:01:19] suddenly the number of rows in this
[00:01:21] matrix, you can look at it that way,
[00:01:23] is 27 * 27. So there's 729 possibilities
[00:01:27] for what could have come in the context.
[00:01:30] If we take three characters as the
[00:01:31] context, suddenly we have
[00:01:34] 20,000 possibilities of context.
[00:01:37] And so that's just way too many rows of
[00:01:40] this matrix. It's way too few counts
[00:01:43] for each possibility and the whole thing
[00:01:45] just kind of explodes and doesn't work
[00:01:47] very well.
[00:01:49] So that's why today we're going to move
[00:01:50] on to this bullet point here and we're
[00:01:52] going to implement a multi-layer
[00:01:53] perceptron model to predict the next uh
[00:01:57] in a sequence. And this modeling
[00:01:59] approach that we're going to adopt
[00:02:00] follows this paper Bengio et al. 2003.
[00:02:04] So, I have the paper pulled up here.
[00:02:06] Now, this isn't the very first paper
[00:02:07] that proposed the use of uh multi-layer
[00:02:10] perceptrons or neural networks to
[00:02:11] predict the next character or token in a
[00:02:13] sequence, but it's definitely one that
[00:02:15] is uh was very influential around that
[00:02:17] time. It is very often cited to stand in
[00:02:19] for this idea, and I think it's a very
[00:02:21] nice write-up. And so, this is the paper
[00:02:23] that we're going to first look at and
[00:02:25] then implement. Now, this paper has 19
[00:02:27] pages. So, we don't have time to go into
[00:02:30] the full detail of this paper, but I
[00:02:31] invite you to read it. Uh it's very
[00:02:33] readable, interesting, and has a lot of
[00:02:34] interesting ideas in it as well.
[00:02:37] In the introduction, they describe the
[00:02:38] exact same problem I just described. And
[00:02:40] then to address it, they propose the
[00:02:42] following model.
[00:02:43] Now, keep in mind that we are building a
[00:02:46] character-level language model. So,
[00:02:48] we're working on the level of
[00:02:49] characters. In this paper, they have a
[00:02:51] vocabulary of 17,000 possible words, and
[00:02:54] they instead built a word-level language
[00:02:56] model. But, we're going to still stick
[00:02:57] with the characters, but we'll take the
[00:02:59] same modeling approach.
[00:03:01] Now, what they do is basically they
[00:03:03] propose to take every one of these
[00:03:04] words, 17,000 words, and they're going
[00:03:07] to associate to each word a say
[00:03:10] 30-dimensional feature vector.
[00:03:12] So, every word is now embedded into a
[00:03:16] 30-dimensional space. You can think of
[00:03:18] it that way. So, we have 17,000 points
[00:03:21] or vectors in a 30-dimensional space,
[00:03:23] and that's um you might imagine that's
[00:03:25] very crowded. That's a lot of points for
[00:03:27] a very small space.
[00:03:28] Now,
[00:03:30] in the beginning, these words are
[00:03:31] initialized completely randomly. So,
[00:03:32] they're spread out at random.
[00:03:34] But, then we're going to tune these
[00:03:36] embeddings of these words using back
[00:03:38] propagation. So, during the course of
[00:03:40] training of this neural network, these
[00:03:42] points or vectors are going to basically
[00:03:43] move around in this space. And you might
[00:03:46] imagine that, for example, words that
[00:03:48] have very similar meanings or that are
[00:03:50] indeed synonyms of each other might end
[00:03:52] up in a very similar part of the space.
[00:03:54] And conversely, words that mean very
[00:03:55] different things would go somewhere else
[00:03:57] in the space.
[00:03:59] Now, their modeling approach otherwise
[00:04:01] is identical to ours. They are using a
[00:04:03] multi-layer neural network to predict
[00:04:04] the next word given the previous words.
[00:04:07] And to train the neural network, they
[00:04:08] are maximizing the log likelihood of the
[00:04:10] training data, just like we did.
[00:04:12] So, the modeling approach itself is
[00:04:14] identical. Now, here they have a
[00:04:16] concrete example of this intuition.
[00:04:18] Why does it work?
[00:04:20] Basically, suppose that for example, you
[00:04:21] are trying to predict "A dog was running
[00:04:23] in a blank."
[00:04:25] Now, suppose that the exact phrase "A
[00:04:27] dog was running in a" has never occurred
[00:04:30] in the training data.
[00:04:31] And here you are at uh sort of test time
[00:04:33] later when the model is deployed
[00:04:35] somewhere.
[00:04:36] And it's trying to make a sentence, and
[00:04:38] it's saying "A dog was running in a
[00:04:40] blank."
[00:04:41] And because it's never encountered this
[00:04:43] exact phrase in the training set, you're
[00:04:45] out of distribution, as we say. Like,
[00:04:47] you don't have fundamentally any
[00:04:49] reason to suspect um
[00:04:52] what might come next.
[00:04:54] But, this approach actually allows you
[00:04:55] to get around that. Because maybe you
[00:04:57] didn't see the exact phrase "A dog was
[00:04:59] running in a something." But, maybe
[00:05:01] you've seen similar phrases. Maybe
[00:05:02] you've seen the phrase "The dog was
[00:05:04] running in a blank."
[00:05:06] And maybe your network has learned that
[00:05:07] A and the are like frequently are
[00:05:10] interchangeable with each other. And so,
[00:05:12] maybe it took the embedding for A and
[00:05:14] the embedding for the, and it actually
[00:05:16] put them like nearby each other in the
[00:05:17] space. And so, you can transfer
[00:05:19] knowledge through that embedding, and
[00:05:21] you can generalize in that way.
[00:05:23] Similarly, the network could know that
[00:05:25] cats and dogs are animals, and they
[00:05:26] co-occur in lots of very similar
[00:05:28] contexts. And so, even though you
[00:05:30] haven't seen this exact phrase,
[00:05:32] or if you haven't seen exactly walking
[00:05:34] or running, you can through the
[00:05:36] embedding space transfer knowledge, and
[00:05:38] you can generalize to novel scenarios.
[00:05:42] So, let's now scroll down to the diagram
[00:05:43] of the neural network. Uh they have a
[00:05:45] nice uh diagram here.
[00:05:47] And in this example, we are taking three
[00:05:49] previous words
[00:05:51] and we are trying to predict the fourth
[00:05:53] word
[00:05:54] in the sequence.
[00:05:56] Now, these three previous words, as I
[00:05:57] mentioned, we have a vocabulary of
[00:05:59] 17,000
[00:06:01] possible words.
[00:06:03] So, every one of these
[00:06:04] basically are the index of the incoming
[00:06:08] word.
[00:06:09] And because there are 17,000 words, this
[00:06:11] is an integer between 0 and 16,999.
[00:06:17] Now, there's also a lookup table that
[00:06:19] they call C.
[00:06:21] This lookup table is a matrix that is
[00:06:22] 17,000 by, say, 30.
[00:06:26] And basically what we're doing here is
[00:06:27] we're treating this as a lookup table.
[00:06:29] And so, every index is plucking out a
[00:06:32] row of this embedding matrix
[00:06:35] so that each index is converted to the
[00:06:37] 30-dimensional vector that corresponds
[00:06:39] to the embedding vector for that word.
[00:06:42] So, here we have the input layer of 30
[00:06:45] neurons for three words, making up 90
[00:06:48] neurons in total.
[00:06:50] And here they're saying that this matrix
[00:06:52] C is shared across all the words. So,
[00:06:54] we're always indexing into the same
[00:06:56] matrix C over and over.
[00:06:59] for each one of these words.
[00:07:02] Next up is the hidden layer of this
[00:07:03] neural network.
[00:07:04] The size of this hidden neural layer of
[00:07:06] this neural net is a hyper parameter.
[00:07:09] So, we use the word hyper parameter when
[00:07:10] it's kind of like a design choice up to
[00:07:12] the designer of the neural net. And this
[00:07:13] can be as large as you'd like or as
[00:07:15] small as you'd like. So, for example,
[00:07:17] the size could be 100.
[00:07:19] And we are going to go over multiple
[00:07:20] choices of the size of this hidden
[00:07:22] layer, and we're going to evaluate how
[00:07:24] well they work.
[00:07:26] So, say there were 100 neurons here,
[00:07:28] all of them would be fully connected to
[00:07:29] the 90 words or 90 um
[00:07:33] numbers that make up these three words.
[00:07:35] So, this is a fully connected layer.
[00:07:38] Then there's a tanh non-linearity.
[00:07:40] And then there's this output layer. And
[00:07:42] because there are 17,000 possible words
[00:07:44] that could come next, this layer has
[00:07:46] 17,000 neurons, and all of them are
[00:07:49] fully connected to all of these neurons
[00:07:52] in the hidden layer.
[00:07:54] So there's a lot of parameters here
[00:07:56] because there's a lot of words. So most
[00:07:58] computation is here. This is the
[00:07:59] expensive layer.
[00:08:01] Now there are 17,000 logits here. So on
[00:08:04] top of there, we have the softmax layer,
[00:08:06] which we've seen in our previous video
[00:08:08] as well. So every one of these logits is
[00:08:10] exponentiated, and then everything is
[00:08:12] normalized to sum to one so that we have
[00:08:15] a nice probability distribution for the
[00:08:17] next word in the sequence.
[00:08:19] Now of course during training, we
[00:08:21] actually have the label. We have the
[00:08:23] identity of the next word in the
[00:08:24] sequence.
[00:08:25] That word or its index is used to pluck
[00:08:29] out the probability of that word,
[00:08:32] and then we are maximizing the
[00:08:34] probability of that word with respect to
[00:08:37] the parameters of this neural net.
[00:08:39] So the parameters are the weights and
[00:08:41] biases of this output layer, the weights
[00:08:44] and biases of this hidden layer, and the
[00:08:47] embedding lookup table C. And all of
[00:08:49] that is optimized using backpropagation.
[00:08:52] And these dashed arrows, ignore those.
[00:08:55] That represents a variation of a neural
[00:08:57] net that we are not going to explore in
[00:08:58] this video.
[00:08:59] So that's the setup, and now let's
[00:09:01] implement it.
[00:09:02] Okay, so I started a brand new notebook
[00:09:04] for this lecture.
[00:09:05] We are importing PyTorch, and we are
[00:09:07] importing Matplotlib so we can create
[00:09:09] figures.
[00:09:10] Then I am reading all the names into a
[00:09:13] list of words like I did before, and I'm
[00:09:15] showing the first eight right here.
[00:09:18] Keep in mind that we have a 32,000 in
[00:09:20] total. These are just the first eight.
[00:09:22] And then here I'm building out the
[00:09:24] vocabulary of characters and all the
[00:09:25] mappings from the characters as strings
[00:09:28] to integers and vice versa.
[00:09:31] Now the first thing we want to do is we
[00:09:32] want to compile the data set for the
[00:09:34] neural network. And I had to rewrite
[00:09:36] this code.
[00:09:37] I'll show you in a second what it looks
[00:09:39] like.
[00:09:41] So this is the code that I created for
[00:09:43] the data set creation. So let me first
[00:09:44] run it and then I'll briefly explain how
[00:09:46] this works.
[00:09:48] So first we're going to define something
[00:09:50] called block size. And this is basically
[00:09:52] the context length of how many
[00:09:54] characters do we take to predict the
[00:09:56] next one. So here in this example we're
[00:09:58] taking three characters to predict the
[00:09:59] fourth one. So we have a block size of
[00:10:02] three. That's the size of the block that
[00:10:04] supports the prediction.
[00:10:06] Then here I'm building out the X and Y.
[00:10:10] The X are the input to the neural net
[00:10:12] and the Y are the labels for each
[00:10:15] example inside X.
[00:10:17] Then I'm iterating over the first five
[00:10:19] words. I'm doing first five just for
[00:10:21] efficiency while we are developing all
[00:10:23] the code. But then later we're going to
[00:10:24] come here and erase this so that we use
[00:10:26] the entire training set.
[00:10:29] So here I'm printing the word Emma.
[00:10:32] And here I'm basically showing the
[00:10:33] examples that we can generate. The five
[00:10:36] examples that we can generate out of the
[00:10:37] single
[00:10:38] serve word Emma.
[00:10:41] So
[00:10:42] when we are given the context of just
[00:10:44] dot dot dot, the first character in a
[00:10:45] sequence is E.
[00:10:47] In this context, the label is M.
[00:10:50] When the context is this, the label is
[00:10:52] M.
[00:10:53] And so forth.
[00:10:54] And so the way I build this out is first
[00:10:56] I start with a padded context of just
[00:10:57] zero tokens.
[00:10:59] Then I iterate over all the characters.
[00:11:01] I get the character in the sequence and
[00:11:04] I basically build out the array Y of
[00:11:07] this current character and the array X
[00:11:09] which stores the current running
[00:11:10] context.
[00:11:11] And then here see I print everything and
[00:11:14] here I
[00:11:15] crop the context and enter the new
[00:11:17] character in the sequence. So this is
[00:11:19] kind of like a rolling window of
[00:11:20] context.
[00:11:22] Now we can change the block size here to
[00:11:24] for example four.
[00:11:25] And in that case we would be predicting
[00:11:27] the fifth character given the previous
[00:11:29] four.
[00:11:30] Or it can be five and then it would look
[00:11:32] like this.
[00:11:34] Or it can be say 10.
[00:11:36] And then it would look something like
[00:11:37] this. We're taking 10 characters to
[00:11:39] predict the 11th one.
[00:11:41] And we're always padding with dots.
[00:11:43] So let me bring this back to three, just
[00:11:45] so that uh we have what we have here in
[00:11:48] the paper.
[00:11:50] And finally, the data set right now
[00:11:51] looks as follows.
[00:11:53] From these five words, we have created a
[00:11:55] data set of 32 examples.
[00:11:57] And each input to the neural net is
[00:11:59] three integers, and we have a label that
[00:12:02] is also an integer, uh Y. So X looks
[00:12:05] like this.
[00:12:06] These are the individual examples.
[00:12:08] And then Y are the labels.
[00:12:12] So
[00:12:13] given this,
[00:12:15] let's now write the neural network that
[00:12:17] takes these X's and predicts the Y's.
[00:12:19] First, let's build the embedding uh look
[00:12:21] up table C.
[00:12:23] So we have 27 possible characters, and
[00:12:25] we're going to embed them in a lower
[00:12:26] dimensional space.
[00:12:28] In the paper, they have 17,000 words,
[00:12:31] and they embed them in uh spaces as
[00:12:33] small dimensional as 30. So they cram
[00:12:36] 17,000 um
[00:12:38] words into 30-dimensional space. In our
[00:12:40] case, we have only 27 possible
[00:12:42] characters, so let's cram them in
[00:12:44] something as small as to start with, for
[00:12:46] example, a two-dimensional space.
[00:12:48] So this look up table will be random
[00:12:50] numbers,
[00:12:51] and we'll have 27 rows, and we'll have
[00:12:54] two columns.
[00:12:56] Right? So each 20 each one of 27
[00:12:58] characters will have a two-dimensional
[00:13:00] embedding.
[00:13:02] So that's our matrix C of embeddings, in
[00:13:05] the beginning initialized randomly.
[00:13:07] Now, before we embed all of the integers
[00:13:10] inside the input X using this look up
[00:13:12] table C,
[00:13:14] let me actually just try to embed a
[00:13:15] single individual integer, like say
[00:13:17] five.
[00:13:19] Um so we get a sense of how this works.
[00:13:21] Now, one way this works, of course, is
[00:13:24] we can just take the C, and we can index
[00:13:26] into row five.
[00:13:28] And that gives us a vector, the fifth
[00:13:30] row of C.
[00:13:31] And um
[00:13:33] this is one way to do it.
[00:13:34] The other way that I presented in the
[00:13:36] previous lecture is actually seemingly
[00:13:38] different, but actually identical.
[00:13:40] So, in the previous lecture, what we did
[00:13:42] is we took these integers and we used
[00:13:43] the one-hot encoding to first encode
[00:13:46] them.
[00:13:46] So, F.one_hot
[00:13:48] we want to encode integer five
[00:13:50] and we want to tell it that the number
[00:13:52] of classes is 27. So, that's the
[00:13:54] 26-dimensional vector of all zeros
[00:13:56] except the fifth bit is turned on.
[00:14:00] Now, this actually doesn't work.
[00:14:03] The reason is that
[00:14:04] this input actually must be a
[00:14:05] torch.tensor.
[00:14:08] And I'm making some of these errors
[00:14:09] intentionally just so you get to see
[00:14:10] some errors and how to fix them.
[00:14:12] Uh so, this must be a tensor not an int,
[00:14:14] fairly straightforward to fix.
[00:14:16] We get a one-hot vector. The fifth
[00:14:18] dimension is one and the shape of this
[00:14:20] is 27.
[00:14:22] And now notice that, just as I briefly
[00:14:24] alluded to in the previous video, if we
[00:14:26] take this one-hot vector and we multiply
[00:14:29] it by C
[00:14:33] then
[00:14:35] um
[00:14:35] what would you expect?
[00:14:37] Well, number one
[00:14:39] first you'd expect an error
[00:14:41] because um
[00:14:43] expected scalar type long but found
[00:14:45] float. So, a little bit confusing, but
[00:14:48] the problem here is that one-hot, the
[00:14:50] data type of it
[00:14:52] is long. It's a 64-bit integer. But,
[00:14:56] this is a float tensor and so PyTorch
[00:14:58] doesn't know how to multiply an int with
[00:15:00] a float and that's why we had to
[00:15:02] explicitly cast this to a float so that
[00:15:04] we can multiply.
[00:15:06] Now, the output actually here
[00:15:09] is identical.
[00:15:11] And that it's identical because of the
[00:15:12] way the matrix uh multiplication here
[00:15:14] works. We have the one-hot um vector
[00:15:17] multiplying columns of C and because of
[00:15:20] all the zeros, they actually end up
[00:15:22] masking out everything in C except for
[00:15:24] the fifth row, which is plucked out.
[00:15:27] And so we actually arrive at the same
[00:15:28] result.
[00:15:30] And that tells you that here we can
[00:15:31] interpret this first piece here, this
[00:15:34] embedding of the integer. We can either
[00:15:36] think of it as the integer indexing into
[00:15:38] a lookup table C.
[00:15:40] But equivalently, we can also think of
[00:15:41] this little piece here as a first layer
[00:15:44] of this bigger neural net.
[00:15:46] This layer here has neurons that have no
[00:15:48] non-linearity, they're no tan h, they're
[00:15:50] just linear neurons, and their weight
[00:15:52] matrix is C.
[00:15:55] And then we are encoding integers into
[00:15:57] one-hot and feeding those into a neural
[00:15:59] net. And this first layer basically
[00:16:01] embeds them.
[00:16:02] So those are two equivalent ways of
[00:16:04] doing the same thing. We're just going
[00:16:06] to index because it's much much faster,
[00:16:08] and we're going to discard this
[00:16:09] interpretation of one-hot inputs into
[00:16:12] neural nets. And we're just going to
[00:16:14] index integers and create and use
[00:16:16] embedding tables. Now, embedding a
[00:16:18] single integer like five is easy enough.
[00:16:20] We can simply ask PyTorch to retrieve
[00:16:22] the fifth row of C. Or the row index
[00:16:25] five of C.
[00:16:27] But how do we simultaneously embed all
[00:16:30] of these 32 by three integers stored in
[00:16:32] array X?
[00:16:34] Luckily, PyTorch indexing is fairly
[00:16:36] flexible and quite powerful. So it
[00:16:39] doesn't just work to um
[00:16:41] ask for a single element five like this.
[00:16:44] You can actually index using lists. So
[00:16:46] for example, we can get the rows five,
[00:16:48] six, and seven, and this will just work
[00:16:51] like this. We can index with a list.
[00:16:53] It doesn't just have to be a list, it
[00:16:55] can also be a actually a tensor of
[00:16:57] integers.
[00:16:58] And we can index with that.
[00:17:00] So this is a integer tensor 567, and
[00:17:03] this will just work as well.
[00:17:06] In fact, we can also, for example,
[00:17:07] repeat row seven and retrieve it
[00:17:09] multiple times. And uh
[00:17:12] that same index will just get embedded
[00:17:14] multiple times here.
[00:17:16] So here we are indexing with a
[00:17:17] one-dimensional
[00:17:19] tensor of integers. But, it turns out
[00:17:21] that you can also index with
[00:17:22] multi-dimensional tensors of integers.
[00:17:25] Here, we have a two-dimensional in
[00:17:27] tensor of integers. So, we can simply
[00:17:29] just do C at X.
[00:17:32] And this just works.
[00:17:34] And the shape of this
[00:17:36] is
[00:17:37] 32 by 3, which is the original shape.
[00:17:40] And now, for every one of those 32 by 3
[00:17:41] integers, we've retrieved the embedding
[00:17:43] vector here.
[00:17:46] So, basically, we have that as an
[00:17:48] example.
[00:17:49] The 13th or example, index 13,
[00:17:53] um the second dimension is the integer
[00:17:56] one as an example.
[00:17:58] And so, here, if we do C of X, which
[00:18:02] gives us that array, and then we index
[00:18:04] into 13 by 2 of that array,
[00:18:07] then we we get the embedding
[00:18:09] here.
[00:18:10] And you can verify that C at one,
[00:18:14] which is the integer at that location,
[00:18:16] is indeed equal to this.
[00:18:20] You see they're equal.
[00:18:21] So, basically, long story short, PyTorch
[00:18:23] indexing is awesome. And to embed
[00:18:26] simultaneously
[00:18:28] all of the integers in X, we can simply
[00:18:30] do C of X. And that is our embedding.
[00:18:33] And that just works.
[00:18:35] Now, let's construct this layer here,
[00:18:37] the hidden layer.
[00:18:38] So, we have that W1, as I'll call it,
[00:18:42] are these weights, which we will
[00:18:44] initialize randomly.
[00:18:46] Now, the number of inputs to this layer
[00:18:48] is going to be 3 * 2, right? Because we
[00:18:51] have two-dimensional embeddings, and we
[00:18:52] have three of them.
[00:18:53] So, the number of inputs is six.
[00:18:56] And the number of neurons in this layer
[00:18:58] is a variable up to us. Let's use 100
[00:19:01] neurons as an example.
[00:19:03] And then, biases will be also
[00:19:05] initialized randomly as an example.
[00:19:07] And let's And we just need 100 of them.
[00:19:11] Now, the problem with this is we can't
[00:19:13] simply Normally, we would take the
[00:19:15] input, in this case that's embedding,
[00:19:17] and we'd like to multiply it with these
[00:19:19] weights.
[00:19:20] And then we would like to add the bias.
[00:19:22] This is roughly what we want to do.
[00:19:24] But the problem here is that these
[00:19:25] embeddings are stacked up in the
[00:19:27] dimensions of this input tensor.
[00:19:29] So, this will not work, this matrix
[00:19:31] multiplication, because this is a shape
[00:19:32] 32 by 3 by 2, and I can't multiply that
[00:19:35] by 6 by 100.
[00:19:37] So, somehow we need to concatenate these
[00:19:40] inputs here together so that we can do
[00:19:41] something along these lines, which
[00:19:43] currently does not work.
[00:19:45] So, how do we transform this 32 by 3 by
[00:19:47] 2 into a 32 by 6 so that we can actually
[00:19:50] perform this uh multiplication over
[00:19:53] here? I'd like to show you that there
[00:19:55] are usually many ways of uh implementing
[00:19:58] what you'd like to do in torch.
[00:20:00] And some of them will be faster, better,
[00:20:02] shorter, etc.
[00:20:03] And that's because torch is a very large
[00:20:06] library, and it's got lots and lots of
[00:20:07] functions. So, if we just go to the
[00:20:09] documentation and click on torch, you'll
[00:20:11] see that my slider here is very tiny,
[00:20:14] and that's because there are so many
[00:20:15] functions that you can call on these
[00:20:16] tensors
[00:20:17] to transform them, create them, multiply
[00:20:20] them, add them, perform all kinds of
[00:20:22] different operations on them.
[00:20:24] And so, this is kind of like
[00:20:28] the space of possibility, if you will.
[00:20:31] Now, one of the things that you can do
[00:20:32] is if we can control here, control F for
[00:20:34] concatenate. And we see that there's a
[00:20:36] function, torch.cat, short for
[00:20:38] concatenate.
[00:20:40] And this concatenates a given sequence
[00:20:42] of tensors in a given dimension.
[00:20:45] And uh these tensors must have the same
[00:20:46] shape, etc. So, we can use the
[00:20:48] concatenate operation to, in a naive
[00:20:51] way, concatenate these three embeddings
[00:20:53] for each input.
[00:20:56] So, in this case, we have emb of
[00:20:58] emb of the shape. And really what we
[00:21:00] want to do is we want to retrieve these
[00:21:02] three parts and concatenate them.
[00:21:05] So, we want to grab all the examples.
[00:21:08] We want to grab
[00:21:10] first the zeroth um
[00:21:13] index and then all of
[00:21:16] this.
[00:21:17] So, this plucks out
[00:21:20] the 32 by 2 embeddings of just the first
[00:21:24] word here.
[00:21:26] And so, basically we want this guy.
[00:21:28] We want the first dimension. And we want
[00:21:31] the second dimension.
[00:21:32] And these are the three pieces
[00:21:34] individually.
[00:21:36] And then we want to treat this as a
[00:21:38] sequence and we want to torch.cat
[00:21:40] on that sequence. So, this is the list.
[00:21:43] torch.cat takes a sequence of tensors.
[00:21:47] And then we have to tell it along which
[00:21:49] dimension to concatenate.
[00:21:51] So, in this case all these are 32 by 2
[00:21:53] and we want to concatenate not across
[00:21:55] dimension zero, but across dimension
[00:21:57] one.
[00:21:58] So, passing in one
[00:22:00] gives us a result.
[00:22:01] The shape of this is 32 by 6 exactly as
[00:22:04] we'd like.
[00:22:05] So, that basically took 32 and squashed
[00:22:08] these by concatenating them into 32 by
[00:22:10] 6.
[00:22:11] Now, this is kind of ugly because this
[00:22:13] code would not generalize if we want to
[00:22:15] later change the block size. Right now,
[00:22:17] we have three inputs.
[00:22:19] Three words. But what if we had five?
[00:22:22] Then here we would have to change the
[00:22:23] code because I'm indexing directly.
[00:22:25] Well, torch comes to rescue again
[00:22:27] because there turns out to be a function
[00:22:29] called unbind.
[00:22:31] And it removes a tensor dimension.
[00:22:35] So, removes a tensor dimension, returns
[00:22:37] a tuple of all slices along a given
[00:22:39] dimension without it.
[00:22:41] So, this is exactly what we need.
[00:22:43] And basically when we call torch.unbind
[00:22:48] torch.unbind
[00:22:50] of emb and passing dimension um one,
[00:22:55] index one.
[00:22:56] This gives us a list of
[00:22:58] um a list of tensors exactly equivalent
[00:23:01] to this.
[00:23:02] So, running this
[00:23:04] gives us a length
[00:23:06] three
[00:23:07] and it's exactly this list. And so, we
[00:23:09] can call torch.cat on it.
[00:23:12] And along the first dimension.
[00:23:15] And this works.
[00:23:16] And the shape is the same.
[00:23:19] But now this is uh it doesn't matter if
[00:23:21] we have block size three or five or 10,
[00:23:23] this will just work.
[00:23:24] So, this is one way to do it. But it
[00:23:26] turns out that in this case, there's
[00:23:28] actually a significantly better and more
[00:23:30] efficient way. And this gives me an
[00:23:32] opportunity to hint at some of the
[00:23:34] internals of torch.tensor.
[00:23:36] So, let's create
[00:23:38] an array here
[00:23:40] of elements from zero to 17. And the
[00:23:42] shape of this
[00:23:44] is just 18. It's a single vector of 18
[00:23:46] numbers.
[00:23:48] It turns out that we can very quickly
[00:23:49] re-represent this as different sized and
[00:23:53] dimensional tensors.
[00:23:54] We do this by calling a view.
[00:23:57] And we can say that actually this is not
[00:23:59] a single vector of 18, this is a 2x9
[00:24:02] tensor.
[00:24:04] Or alternatively, this is a 9x2 tensor.
[00:24:08] Or this is actually a 3x3x2 tensor.
[00:24:11] As long as the total number of elements
[00:24:13] here multiply to be the same, uh this
[00:24:16] will just work.
[00:24:18] And in PyTorch, this operation calling
[00:24:21] dot view is extremely efficient.
[00:24:24] And the reason for that is that in each
[00:24:26] tensor, there's something called the
[00:24:28] underlying storage.
[00:24:30] And the storage is just the numbers
[00:24:32] always as a one-dimensional vector. And
[00:24:34] this is how this tensor is represented
[00:24:37] in the computer memory. It's always a
[00:24:38] one-dimensional vector.
[00:24:41] But when we call that view, we are
[00:24:44] manipulating some of attributes of that
[00:24:46] tensor that dictate how this
[00:24:48] one-dimensional sequence is interpreted
[00:24:51] to be an N-dimensional tensor.
[00:24:53] And so, what's happening here is that no
[00:24:55] memory is being changed, copied, moved,
[00:24:57] or created when we call dot view. The
[00:24:59] The storage
[00:25:00] is identical, but when you call dot
[00:25:02] view, some of the internal um
[00:25:05] attributes of the view of this tensor
[00:25:07] are being manipulated and changed. In
[00:25:09] particular, there's something There's
[00:25:10] something called a storage offset,
[00:25:12] strides, and shapes, and those are
[00:25:14] manipulated so that this one-dimensional
[00:25:16] sequence of bytes is seen as different
[00:25:18] n-dimensional arrays.
[00:25:20] There's a blog post here from Eric
[00:25:22] called PyTorch Internals, where he goes
[00:25:25] into some of this with respect to tensor
[00:25:27] and how the view of a tensor is
[00:25:29] represented.
[00:25:30] And this is really just like a logical
[00:25:32] construct of representing the physical
[00:25:34] memory.
[00:25:35] And uh so this is a pretty good um
[00:25:38] blog post that you can go into. I might
[00:25:39] also create an entire video on the
[00:25:41] internals of torch tensor and how this
[00:25:42] works.
[00:25:44] For here, we just note that this is an
[00:25:46] extremely efficient operation.
[00:25:48] And if I delete this and come back to
[00:25:50] our emb,
[00:25:53] we see that the shape of our emb is 32
[00:25:55] by 3 by 2, but we can simply ask for
[00:25:58] PyTorch to view this instead as a 32 by
[00:26:01] 6.
[00:26:03] And the way this gets flattened into a
[00:26:05] 32 by 6 array
[00:26:07] just happens that
[00:26:09] these two
[00:26:10] get stacked up in a single row. And so
[00:26:13] that's basically the concatenation
[00:26:15] operation that we're after.
[00:26:17] And you can verify that this actually
[00:26:18] gives the exact same result as what we
[00:26:20] had before.
[00:26:22] So this is an element-wise equals, and
[00:26:23] you can see that all the elements of
[00:26:25] these two tensors are the same.
[00:26:27] And so we get the exact same result.
[00:26:30] So long story short, we can actually
[00:26:32] just come here,
[00:26:34] and if we just view this as a 32 by 6
[00:26:38] um instead, then this multiplication
[00:26:40] will work and give us the hidden states
[00:26:43] that we're after.
[00:26:44] So if this is H,
[00:26:46] then H.shape is now the 100-dimensional
[00:26:49] activations for every one of our 32
[00:26:52] examples.
[00:26:53] And this gives the desired result. Let
[00:26:55] me do two things here. Number one, let's
[00:26:57] not use 32. We can, for example, do
[00:27:00] something like
[00:27:01] um
[00:27:02] emb.shape
[00:27:04] at zero.
[00:27:05] So that we don't hardcode these numbers.
[00:27:07] And this would work for any size of this
[00:27:09] emb.
[00:27:10] Or alternatively, we can also do -1.
[00:27:12] When we do -1, PyTorch will infer what
[00:27:15] this should be.
[00:27:16] Because the number of elements must be
[00:27:17] the same, and we're saying that this is
[00:27:19] six, PyTorch will derive that this must
[00:27:21] be 32 or whatever else it is if emb is
[00:27:24] of different size.
[00:27:26] The other thing is here,
[00:27:28] um
[00:27:29] one more thing I'd like to point out is
[00:27:33] here when we do the concatenation,
[00:27:35] this actually is much less efficient
[00:27:37] because um this concatenation would
[00:27:39] create a whole new tensor with a whole
[00:27:41] new storage. So new memory is being
[00:27:43] created because there's no way to
[00:27:44] concatenate tensors just by manipulating
[00:27:47] the view attributes. So this is
[00:27:49] inefficient and creates all kinds of new
[00:27:50] memory.
[00:27:52] Uh so let me delete this now.
[00:27:55] We don't need this.
[00:27:57] And here to calculate H, we want to also
[00:27:59] dot tanh
[00:28:01] of this to get our
[00:28:04] oops, to get our H.
[00:28:07] So these are now numbers between -1 and
[00:28:08] 1 because of the tanh.
[00:28:10] And we have that the shape is 32 by 100.
[00:28:14] And that is basically this hidden layer
[00:28:16] of activations here
[00:28:17] for every one of our 32 examples.
[00:28:20] Now there's one more thing I glossed
[00:28:21] over that we have to be very careful
[00:28:23] with, and that's this and that's this
[00:28:25] plus here.
[00:28:26] In particular, we want to make sure that
[00:28:27] the broadcasting will do what we like.
[00:28:30] The shape of this is 32 by 100, and B1's
[00:28:33] shape is 100.
[00:28:35] So we see that the addition here will
[00:28:37] broadcast these two. And in particular,
[00:28:39] we have 32 by 100 broadcasting to 100.
[00:28:44] So broadcasting will align on the right,
[00:28:47] create a fake dimension here.
[00:28:49] So, this will become a 1 by 100 row
[00:28:50] vector.
[00:28:52] And then it will copy vertically
[00:28:54] for every one of these rows of 32 and do
[00:28:57] an element-wise addition.
[00:28:58] So, in this case, the correct thing will
[00:29:00] be happening because the same bias
[00:29:02] vector
[00:29:03] will be added to all the rows
[00:29:05] of
[00:29:06] this matrix.
[00:29:08] So, that is correct. That's what we'd
[00:29:09] like. And uh it's always good practice
[00:29:11] to just make sure uh so that you don't
[00:29:13] shoot yourself in the foot. And finally,
[00:29:15] let's create the final layer here.
[00:29:17] So, let's create
[00:29:19] W2 and B2.
[00:29:22] The input now is 100.
[00:29:25] And the output number of neurons will be
[00:29:27] for us 27 because we have 27 possible
[00:29:29] characters that come next.
[00:29:31] So, the biases will be 27 as well.
[00:29:35] So, therefore, the logits, which are the
[00:29:36] outputs of this neural net,
[00:29:38] are going to be um
[00:29:41] H multiplied by W2 plus B2.
[00:29:47] Logits.shape is 32 by 27.
[00:29:50] And the logits look
[00:29:52] good. Now, exactly as we saw in the
[00:29:54] previous video, we want to take these
[00:29:55] logits and we want to first exponentiate
[00:29:58] them to get our fake counts.
[00:30:00] And then we want to normalize them into
[00:30:01] a probability.
[00:30:03] So, prob is counts.divide.
[00:30:05] And now uh counts.sum
[00:30:09] along the first dimension and keep dims
[00:30:11] as true, exactly as in the previous
[00:30:12] video.
[00:30:14] And so,
[00:30:16] prob.shape now is 32 by 27.
[00:30:20] And you'll see that every row of prob
[00:30:23] sums to one, so it's normalized.
[00:30:26] So, that gives us the probabilities.
[00:30:28] Now, of course, we have the actual
[00:30:29] letter that comes next. And that comes
[00:30:31] from this array Y,
[00:30:34] which we which we created during the
[00:30:36] data set creation. So, Y is this last
[00:30:39] piece here, which is the identity of the
[00:30:40] next character in the sequence that we'd
[00:30:42] like to now predict.
[00:30:44] So, what we'd like to do now is just as
[00:30:46] in the previous video, we'd like to
[00:30:48] index into the rows of prob, and each
[00:30:50] row we'd like to pluck out the
[00:30:52] probability assigned to the correct
[00:30:54] character
[00:30:55] as given here.
[00:30:57] So, first we have torch.arange of 32,
[00:31:00] which is kind of like a iterator over um
[00:31:03] numbers from 0 to 31,
[00:31:05] and then we can index into prob in the
[00:31:07] following way.
[00:31:09] prob in torch.arange of 32, which
[00:31:12] iterates the rows. And then in each row,
[00:31:14] we'd like to grab this column as given
[00:31:17] by Y.
[00:31:19] So, this gives the current probabilities
[00:31:21] as assigned by this neural network with
[00:31:23] this setting of its weights
[00:31:25] to the correct character in the
[00:31:26] sequence.
[00:31:27] And you can see here that this looks
[00:31:29] okay for some of these characters. Like
[00:31:31] this is basically 0.2,
[00:31:33] but it doesn't look very good at all for
[00:31:34] many other characters. Like this is
[00:31:36] 0.0701
[00:31:38] probability. And so, the network thinks
[00:31:40] that some of these are extremely
[00:31:42] unlikely. But of course, we haven't
[00:31:43] trained the neural network yet. So,
[00:31:46] um this will improve, and ideally all of
[00:31:49] these numbers here of course are one
[00:31:50] because then we are correctly predicting
[00:31:52] the next character.
[00:31:53] Now, just as in the previous video, we
[00:31:55] want to take these probabilities, we
[00:31:57] want to look at the log probability, and
[00:31:59] then we want to look at the average log
[00:32:01] probability,
[00:32:02] and then negative of it to create the
[00:32:04] negative log likelihood loss.
[00:32:07] So, the loss here is 17.
[00:32:10] And this is the loss that we'd like to
[00:32:11] minimize to get the network to predict
[00:32:14] the correct character in the sequence.
[00:32:16] Okay, so I rewrote everything here and
[00:32:18] made it a bit more respectable.
[00:32:20] So, here's our data set.
[00:32:22] Here's all the parameters that we
[00:32:23] defined.
[00:32:24] I'm now using a generator to make it
[00:32:26] reproducible.
[00:32:27] I clustered all the parameters into a
[00:32:29] single list of parameters, so that for
[00:32:31] example, it's easy to count them and see
[00:32:33] that in total we currently have about
[00:32:34] 3,400 parameters.
[00:32:37] And this is the forward pass as we
[00:32:38] developed it.
[00:32:39] And we arrive at a single number here,
[00:32:42] the loss, that is currently expressing
[00:32:44] how well this neural network works with
[00:32:46] the current setting of parameters.
[00:32:48] Now, I would like to make it even more
[00:32:50] respectable.
[00:32:51] So, in particular, see these lines here,
[00:32:53] where we take the logits and we
[00:32:54] calculate the loss.
[00:32:57] Um we're not actually reinventing the
[00:32:59] wheel here. This is just um
[00:33:01] classification, and many people use
[00:33:03] classification, and that's why there is
[00:33:05] a functional.cross_entropy function in
[00:33:07] PyTorch to calculate this much more
[00:33:09] efficiently.
[00:33:10] So, we could just simply call
[00:33:11] f.cross_entropy,
[00:33:13] and we can pass in the logits, and we
[00:33:14] can pass in the
[00:33:16] uh array of targets, Y.
[00:33:18] And this calculates the exact same loss.
[00:33:21] Um so, in fact, we can simply put this
[00:33:24] here
[00:33:25] and erase these three lines, and we're
[00:33:27] going to get the exact same result. Now,
[00:33:30] there are actually many good reasons to
[00:33:31] prefer f.cross_entropy over rolling your
[00:33:34] own implementation like this. I did this
[00:33:36] for educational reasons, but you'd never
[00:33:38] use this in practice. Why is that?
[00:33:40] Number one, when you use
[00:33:41] f.cross_entropy, PyTorch will not
[00:33:43] actually create all these intermediate
[00:33:45] tensors, because these are all new
[00:33:47] tensors in memory, and all this is
[00:33:49] fairly inefficient to run like this.
[00:33:52] Instead, PyTorch will cluster up all
[00:33:54] these operations and very often create
[00:33:57] have a fused kernels that very
[00:33:59] efficiently evaluate these expressions
[00:34:00] that are sort of like clustered uh
[00:34:02] mathematical operations.
[00:34:04] Number two, the backward pass can be
[00:34:06] made much more efficient. And not just
[00:34:08] because it's a fused kernel, but also
[00:34:10] analytically and mathematically, it's
[00:34:12] much it's often a very much uh simpler
[00:34:15] backward pass to implement.
[00:34:17] We actually saw this with micrograd.
[00:34:19] You see here when we implemented tanh,
[00:34:21] the forward pass of this operation to
[00:34:23] calculate the tanh was actually a fairly
[00:34:25] complicated mathematical expression.
[00:34:28] But because it's a clustered
[00:34:29] mathematical expression, when we did the
[00:34:31] backward pass, we didn't individually
[00:34:33] backward through the exp and the two
[00:34:35] times and the minus one and the
[00:34:36] division, etc. We just said it's 1 - t
[00:34:39] squared. And that's a much simpler
[00:34:41] mathematical expression.
[00:34:43] And we were able to do this because
[00:34:44] we're able to reuse calculations and
[00:34:46] because we are able to mathematically
[00:34:48] and analytically derive the derivative
[00:34:50] and often that expression simplifies
[00:34:52] mathematically. And so there's much less
[00:34:54] to implement.
[00:34:56] So not only can can it be made more
[00:34:57] efficient because it runs in a fused
[00:34:59] kernel, but also because the expressions
[00:35:01] can take a much simpler form
[00:35:03] mathematically.
[00:35:06] So that's number one. Number two,
[00:35:08] under the hood, after cross entropy can
[00:35:10] also be significantly more
[00:35:12] um
[00:35:13] numerically well-behaved. Let me show
[00:35:15] you an example of how this works.
[00:35:19] Suppose we have a logits of -2, 3, -3,
[00:35:22] 0, and 5.
[00:35:24] And then we are taking the exponent of
[00:35:25] it and normalizing it to sum to one. So
[00:35:28] when logits take on these values,
[00:35:30] everything is well and good and we get a
[00:35:31] nice probability distribution.
[00:35:33] Now consider what happens when some of
[00:35:35] these logits take on more extreme values
[00:35:37] and that can happen during optimization
[00:35:39] of a neural network.
[00:35:40] Suppose that some of these numbers grow
[00:35:42] very negative, like say -100.
[00:35:45] Then actually everything will come out
[00:35:47] fine. We still get the probabilities
[00:35:48] that um you know, are well-behaved and
[00:35:52] they sum to one and everything is great.
[00:35:54] But because of the way the exp works, if
[00:35:56] you have very positive logits, like say
[00:35:58] positive 100 in here,
[00:36:00] you actually start to run into trouble
[00:36:02] and we get not a number here.
[00:36:04] And the reason for that is that these
[00:36:06] counts
[00:36:08] have an inf here.
[00:36:10] So if you pass in a very negative number
[00:36:12] to exp, you just get a very negative
[00:36:15] Sorry, not negative, but very small
[00:36:16] number, very very near zero and that's
[00:36:18] fine.
[00:36:20] But if you pass in a very positive
[00:36:21] number, suddenly we run out of range in
[00:36:23] our floating point number that
[00:36:25] represents these counts.
[00:36:28] So basically we're taking E and we're
[00:36:29] raising it to the power of 100 and that
[00:36:32] gives us inf because we run out of
[00:36:34] dynamic range on this floating point
[00:36:35] number that is count.
[00:36:38] And so, we cannot pass very large logits
[00:36:41] through this expression.
[00:36:43] Now, let me reset these numbers to
[00:36:45] something reasonable.
[00:36:47] The way PyTorch solves this is that you
[00:36:50] see how we have a well-behaved result
[00:36:52] here.
[00:36:53] It turns out that because of the
[00:36:54] normalization here, you can actually
[00:36:56] offset logits by any arbitrary constant
[00:36:59] value that you want. So, if I add one
[00:37:01] here,
[00:37:02] you actually get the exact same result.
[00:37:04] Or if I add two,
[00:37:06] or if I subtract three.
[00:37:08] Any offset will produce the exact same
[00:37:10] probabilities.
[00:37:12] So, because negative numbers are okay,
[00:37:15] but positive numbers can actually
[00:37:16] overflow this exp, what PyTorch does is
[00:37:19] it internally calculates the maximum
[00:37:21] value that occurs in the logits and it
[00:37:23] subtracts it. So, in this case it would
[00:37:25] subtract five.
[00:37:27] And so, therefore the greatest number in
[00:37:28] logits will become zero and all the
[00:37:30] other numbers will become some negative
[00:37:32] numbers.
[00:37:33] And then the result of this is always
[00:37:35] well-behaved. So, even if we have a 100
[00:37:37] here previously,
[00:37:39] not good, but because PyTorch will
[00:37:41] subtract 100, this will work.
[00:37:44] And so, there's many good reasons to
[00:37:46] call cross entropy. Number one, the
[00:37:49] forward pass can be much more efficient.
[00:37:50] The backward pass can be much more
[00:37:52] efficient. And also things can be much
[00:37:54] more numerically well-behaved. Okay, so
[00:37:56] let's now set up the training of this
[00:37:58] neural net.
[00:37:59] We have the forward pass.
[00:38:02] Uh we don't need these. Except we have
[00:38:05] the loss is equal to the after cross
[00:38:07] entropy. That's the forward pass.
[00:38:09] Then we need the backward pass. First we
[00:38:12] want to set the gradients to be zero.
[00:38:14] So, for P and parameters, we want to
[00:38:16] make sure that P.grad is none, which is
[00:38:18] the same as setting it to zero in
[00:38:19] PyTorch.
[00:38:21] And then loss.backward to populate those
[00:38:23] gradients.
[00:38:24] Once we have the gradients, we can do
[00:38:25] the parameter update. So, for P in
[00:38:27] parameters, we want to take all the data
[00:38:30] and we want to nudge it
[00:38:32] learning rate times p.grad.
[00:38:36] And then we want to repeat this
[00:38:39] a few times.
[00:38:41] Um
[00:38:44] And let's print the loss here as well.
[00:38:48] Now, this won't suffice and will create
[00:38:50] an error because we also have to go for
[00:38:52] P in parameters
[00:38:54] and we have to make sure that
[00:38:55] p.requires_grad
[00:38:57] is set to true in PyTorch.
[00:38:59] And this should just work.
[00:39:03] Okay. So, we started off with loss of 17
[00:39:05] and we're decreasing it.
[00:39:08] Let's run longer.
[00:39:10] And you see how the loss decreases
[00:39:12] a lot here. So,
[00:39:17] if we just run for 1,000 times, we get a
[00:39:20] very, very low loss. And that means that
[00:39:21] we're making very good predictions. Now,
[00:39:23] the reason that this is so
[00:39:25] straightforward right now is because
[00:39:27] we're only um
[00:39:29] overfitting 32 examples.
[00:39:32] So, we only have 32 examples uh of the
[00:39:34] first five words
[00:39:36] and therefore it's very easy to make
[00:39:38] this neural net fit only these two 32
[00:39:40] examples because we have 3,400
[00:39:43] parameters and only 32 examples. So,
[00:39:46] we're doing what's called overfitting a
[00:39:47] single batch of the data
[00:39:50] and getting a very low loss and good
[00:39:52] predictions. Um but that's just because
[00:39:54] we have so many parameters for so few
[00:39:56] examples. So, it's easy to uh make this
[00:39:58] be very low.
[00:40:00] Now, we're not able to achieve exactly
[00:40:01] zero. And the reason for that is we can,
[00:40:04] for example, look at the logits which
[00:40:06] are being predicted.
[00:40:08] And uh we can look at the max along the
[00:40:11] first dimension.
[00:40:13] And in PyTorch, uh max reports both the
[00:40:16] actual values that take on the maximum
[00:40:19] uh, number, but also the indices of
[00:40:20] these.
[00:40:22] And you'll see that the indices are very
[00:40:23] close to the labels.
[00:40:26] But in some cases they differ. For
[00:40:28] example, in this very first example, uh,
[00:40:31] the predicted index is 19, but the label
[00:40:33] is five.
[00:40:35] And we're not able to make loss be zero,
[00:40:37] and fundamentally that's because here
[00:40:40] the very first or the zeroth index is
[00:40:43] the example where dot dot dot is
[00:40:44] supposed to predict E. But you see how
[00:40:46] dot dot dot is also supposed to predict
[00:40:48] an O. And dot dot dot is also supposed
[00:40:50] to predict an I, and then S as well. And
[00:40:53] so basically E, O, A, or S are all
[00:40:56] possible outcomes in the training set
[00:40:58] for the exact same input. So we're not
[00:41:00] able to completely overfit and um,
[00:41:03] and make the loss be exactly zero. Uh,
[00:41:06] so but we're getting very close in the
[00:41:08] cases where uh, there's a unique input
[00:41:11] for a unique output. In those cases we
[00:41:13] do what's called overfit, and we
[00:41:15] basically get the exact same and the
[00:41:16] exact correct result.
[00:41:18] So now all we have to do
[00:41:21] is we just need to make sure that we
[00:41:22] read in the full data set and optimize
[00:41:24] the neural net.
[00:41:25] Okay, so let's swing back up where we
[00:41:27] created the data set.
[00:41:29] And we see that here we only use the
[00:41:30] first five words. So let me now erase
[00:41:32] this,
[00:41:33] and let me erase the print statements,
[00:41:35] otherwise we'll be printing way too
[00:41:36] much.
[00:41:38] And so when we process the full data set
[00:41:40] of all the words, we now have 228,000
[00:41:43] examples instead of just 32.
[00:41:45] So let's now scroll back down. The
[00:41:47] dataset is much larger. We initialize
[00:41:49] the weights, the same number of
[00:41:51] parameters. They all require gradients.
[00:41:54] And then let's push this print out loss
[00:41:56] dot item to be here.
[00:41:58] And let's just see how the optimization
[00:41:59] goes if we run this.
[00:42:04] Okay, so we started with a fairly high
[00:42:05] loss, and then as we're optimizing, the
[00:42:07] loss is coming down.
[00:42:11] But you'll notice that it takes quite a
[00:42:13] bit of time for every single iteration.
[00:42:15] So, let's actually address that. Because
[00:42:17] we're doing way too much work forwarding
[00:42:19] and backwarding 220,000 examples.
[00:42:22] In practice, what people usually do is
[00:42:24] they perform forward and backward pass
[00:42:26] and update on mini batches of the data.
[00:42:29] So, what we will want to do is we want
[00:42:31] to randomly select some portion of the
[00:42:33] data set, and that's a mini batch, and
[00:42:35] then only forward backward and update on
[00:42:37] that little mini batch. And then, um,
[00:42:40] we iterate on those mini batches.
[00:42:42] So, in PyTorch, we can, for example, use
[00:42:43] torch.randint.
[00:42:45] We can generate numbers between 0 and 5
[00:42:47] and make 32 of them.
[00:42:51] Um,
[00:42:52] I believe the size has to be a tuple
[00:42:56] in PyTorch.
[00:42:57] So, we can have a tuple 32 of numbers
[00:43:00] between 0 and 5. But, actually, we want
[00:43:02] x.shape of 0 here.
[00:43:05] And so, this creates uh integers that
[00:43:08] index into our data set, and there's 32
[00:43:10] of them.
[00:43:11] So, if our mini batch size is 32, then
[00:43:13] we can come here and we can first do uh
[00:43:16] mini batch
[00:43:18] construct.
[00:43:20] So, in the integers that we want to
[00:43:22] optimize in this
[00:43:23] um single iteration are in the ix.
[00:43:27] And then, we want to index into x with
[00:43:31] ix to only grab those rows.
[00:43:34] So, we're only getting 32 rows of x.
[00:43:37] And therefore, embeddings will again be
[00:43:38] 32 by 3 by 2, not 200,000 by 3 by 2.
[00:43:43] And then, this ix has to be used not
[00:43:44] just to index into x, but also to index
[00:43:48] into y.
[00:43:50] And now, this should be mini batches,
[00:43:52] and this should be much much faster. So,
[00:43:55] Okay, so it's instant almost.
[00:43:58] So, this way, we can run many many
[00:44:00] examples
[00:44:01] nearly instantly and decrease the loss
[00:44:03] much much faster.
[00:44:05] Now, because we're only dealing with
[00:44:06] mini batches, the quality of our
[00:44:08] gradient is lower. So, the direction is
[00:44:11] not as reliable. It's not the actual
[00:44:13] gradient direction.
[00:44:14] But, the gradient direction is good
[00:44:16] enough even when it's estimating on only
[00:44:18] 32 examples that it is useful.
[00:44:21] And so, it's much better to have an
[00:44:24] approximate gradient and just make more
[00:44:25] steps than it is to evaluate the exact
[00:44:28] gradient and take fewer steps. So,
[00:44:30] that's why in practice,
[00:44:32] uh this works quite well.
[00:44:34] So, let's continue the optimization.
[00:44:38] Let me take out this loss.item from here
[00:44:41] and uh place it over here at the end.
[00:44:46] Okay, so we're hovering around 2.5 or
[00:44:48] so.
[00:44:49] Um
[00:44:50] however, this is only the loss for that
[00:44:51] mini batch. So, let's actually evaluate
[00:44:53] the loss
[00:44:55] here
[00:44:56] for all of X
[00:44:58] and for all of Y, just so we have a full
[00:45:01] sense of exactly how well the model is
[00:45:03] doing right now.
[00:45:05] So, right now we're at about 2.7 on the
[00:45:07] entire training set.
[00:45:09] So, let's run the optimization for a
[00:45:11] while.
[00:45:12] Okay, we're at 2.6.
[00:45:15] 2.57
[00:45:17] 2.53
[00:45:22] Okay.
[00:45:22] So, one issue, of course, is we don't
[00:45:24] know if we're stepping too slow or too
[00:45:27] fast.
[00:45:28] Um so, this point one, I just guessed
[00:45:30] it. So, one question is, how do you
[00:45:32] determine this learning rate?
[00:45:34] And um how do we gain confidence that
[00:45:37] we're stepping in the right um
[00:45:39] sort of speed? So, I'll show you one way
[00:45:41] to determine a reasonable learning rate.
[00:45:43] It works as follows. Let's reset our
[00:45:46] parameters
[00:45:47] to the initial
[00:45:49] um
[00:45:49] settings.
[00:45:51] And now, let's
[00:45:52] print in every step.
[00:45:55] But, let's only do 10 steps or so.
[00:45:58] Or maybe maybe 100 steps.
[00:46:01] We want to find like a very reasonable
[00:46:02] set
[00:46:03] search range, if you will. So, for
[00:46:05] example, if this is like very low,
[00:46:07] then
[00:46:10] we see that the loss is barely
[00:46:11] decreasing. So, that's not
[00:46:13] That's like too low, basically. So,
[00:46:15] let's try
[00:46:16] this one.
[00:46:18] Okay, so we're decreasing the loss, but
[00:46:20] like not very quickly. So, that's a
[00:46:21] pretty good low range.
[00:46:23] Now, let's reset it again.
[00:46:26] And now, let's try to find the place at
[00:46:27] which the loss kind of explodes.
[00:46:29] Uh so, maybe at -1.
[00:46:33] Okay, we see that we're minimizing the
[00:46:34] loss, but you see how it's kind of
[00:46:36] unstable. It goes up and down quite a
[00:46:38] bit.
[00:46:39] Um so, -1 is probably like a fast
[00:46:42] learning rate. Let's try -10.
[00:46:45] Okay, so this isn't optimizing. This is
[00:46:48] not working very well. So, -10 is way
[00:46:50] too big. -1 was already kind of big. Um
[00:46:54] so, therefore, -1 was like somewhat
[00:46:57] reasonable if I reset.
[00:47:00] So, I'm thinking that the right learning
[00:47:01] rate is somewhere between
[00:47:03] um -0.001
[00:47:05] and um
[00:47:07] -1.
[00:47:08] So, the way we can do this here is we
[00:47:09] can use uh torch.linspace.
[00:47:13] And we want to basically do something
[00:47:14] like this, between 0 and 1, but
[00:47:17] um
[00:47:19] uh number of steps is one more parameter
[00:47:21] that's required. Let's do 1,000 steps.
[00:47:23] This creates 1,000
[00:47:26] um numbers between 0.001 and 1.
[00:47:29] But, it doesn't really make sense to
[00:47:31] step between these linearly. So,
[00:47:33] instead, let me create learning rate
[00:47:35] exponent.
[00:47:36] And instead of 0.001, this will be a -3,
[00:47:40] and this will be a 0. And then, the
[00:47:42] actual uh LRs that we want to search
[00:47:44] over are going to be 10 to the power of
[00:47:46] LRE.
[00:47:48] So, now what we're doing is we're
[00:47:49] stepping linearly between the exponents
[00:47:51] of these learning rates. This is 0.001,
[00:47:54] and this is 1, because uh 10 to the
[00:47:56] power of zero is one.
[00:47:58] And therefore, we are spaced
[00:48:00] exponentially in this interval.
[00:48:02] So, these are the candidate learning
[00:48:03] rates
[00:48:04] that we want to sort of like search
[00:48:06] over, roughly.
[00:48:07] So, now what we're going to do is
[00:48:10] here, we are going to run the
[00:48:12] optimization for 1,000 steps.
[00:48:14] And instead of using a fixed number, we
[00:48:17] are going to use learning rate
[00:48:19] indexing into here, lrs of I, and make
[00:48:22] this I.
[00:48:25] So, basically, let me reset this to be,
[00:48:28] again, starting from random,
[00:48:30] creating these learning rates between
[00:48:32] negative um 0.0 between 0.001 and um
[00:48:36] one, but exponentially stepped.
[00:48:39] And here what we're doing is we're
[00:48:41] iterating a thousand times. We're going
[00:48:43] to use the learning rate
[00:48:45] um that's in the beginning very, very
[00:48:47] low. In the beginning, it's going to be
[00:48:49] 0.001, but by the end, it's going to be
[00:48:52] one.
[00:48:53] And then we're going to step with that
[00:48:55] learning rate.
[00:48:57] And now what we want to do is we want to
[00:48:58] keep track of the uh um
[00:49:04] learning rates that we used, and we want
[00:49:06] to look at the losses that resulted.
[00:49:09] And so here, let me
[00:49:12] track stats.
[00:49:14] So, lri.append lr,
[00:49:16] and um
[00:49:18] loss i.append
[00:49:20] loss.item.
[00:49:22] Okay.
[00:49:23] So, again, reset everything,
[00:49:27] and then run.
[00:49:30] And so, basically, we started with a
[00:49:31] very low learning rate, and we went all
[00:49:33] the way up to uh learning rate of
[00:49:34] negative one. And now what we can do is
[00:49:37] we can plt.plot,
[00:49:39] and we can plot the two. So, we can plot
[00:49:41] the learning rates on the x-axis, and
[00:49:43] the losses we saw on the y-axis.
[00:49:46] And often, you're going to find that
[00:49:47] your plot looks something like this,
[00:49:50] where in the beginning, um
[00:49:52] you had very low learning rates. We
[00:49:53] basically anything
[00:49:55] barely anything happened.
[00:49:56] Then we got to like a nice spot here.
[00:50:00] And then as we increase the learning
[00:50:01] rate enough, uh, we basically started to
[00:50:03] be kind of unstable here.
[00:50:05] So a good learning rate turns out to be
[00:50:07] somewhere around here.
[00:50:10] Um, and because we have LRI here,
[00:50:13] um,
[00:50:14] we actually may want to, um,
[00:50:19] do not LR, uh,
[00:50:21] not the learning rate, but the exponent.
[00:50:22] So that would be the LRE at I is maybe
[00:50:25] what we want to log. So let me reset
[00:50:27] this and redo that calculation.
[00:50:30] But now on the x-axis we have the, um,
[00:50:34] exponent of the learning rate. And so we
[00:50:36] can see the exponent of the learning
[00:50:37] rate that is good to use. It would be
[00:50:38] sort of like roughly in the valley here,
[00:50:41] because here the learning rates are just
[00:50:42] way too low. And then here where we
[00:50:44] expect relatively good learning rate
[00:50:46] somewhere here. And then here things are
[00:50:47] starting to explode. So somewhere around
[00:50:50] -1 as the exponent of the learning rate
[00:50:52] is a pretty good setting. And 10 to the
[00:50:55] -1 is .1. So .1 is actually .1 was
[00:50:59] actually a fairly good learning rate
[00:51:01] around here.
[00:51:02] And that's what we had in the initial
[00:51:03] setting.
[00:51:04] Um, but that's roughly how you would
[00:51:06] determine it.
[00:51:07] And so here now we can take out the
[00:51:10] tracking of these.
[00:51:12] And we can just simply set LR to be 10
[00:51:15] to the -1 or
[00:51:18] basically otherwise .1 as it was before.
[00:51:20] And now we have some confidence that
[00:51:21] this is actually a fairly good learning
[00:51:23] rate.
[00:51:24] And so now we can do is we can crank up
[00:51:26] the iterations.
[00:51:27] We can reset our optimization.
[00:51:30] And, um,
[00:51:32] we can run for a pretty long time using
[00:51:34] this learning rate.
[00:51:36] Oops, and we don't want to print. That's
[00:51:38] way too much printing.
[00:51:40] So let me again reset.
[00:51:42] And run 10,000 steps.
[00:51:48] Okay, so we're at 0.2 2.48 roughly.
[00:51:51] Let's run another 10,000 steps.
[00:51:58] 2.46
[00:52:00] And now let's do one learning rate
[00:52:01] decay. What this means is we're going to
[00:52:03] take our learning rate and we're going
[00:52:04] to 10x lower it. And so we're at the
[00:52:07] late stages of training potentially and
[00:52:10] we may want to go uh a bit slower.
[00:52:12] Let's do one more actually at 0.1 just
[00:52:14] to see if
[00:52:17] we're making a dent here.
[00:52:19] Okay, we're still making dent. And by
[00:52:20] the way, the bigram loss that we
[00:52:23] achieved last video was 2.45. So we've
[00:52:26] already surpassed the bigram model.
[00:52:29] And once I get a sense that this is
[00:52:30] actually kind of starting to plateau
[00:52:31] off, uh people like to do as I mentioned
[00:52:33] this learning rate decay. So let's try
[00:52:36] to decay the loss,
[00:52:37] uh the learning rate I mean.
[00:52:42] And we achieve at about 2.3 now.
[00:52:46] Obviously, this is janky and not exactly
[00:52:48] how you would train it in production,
[00:52:50] but this is roughly what you're going
[00:52:51] through. You first find a decent
[00:52:53] learning rate using the approach that I
[00:52:54] showed you.
[00:52:55] Then you start with that learning rate
[00:52:57] and you train for a while.
[00:52:58] And then at the end people like to do a
[00:53:00] learning rate decay where you decay the
[00:53:02] learning rate by say a factor of 10 and
[00:53:04] you do a few more steps and then you get
[00:53:06] a trained network, roughly speaking.
[00:53:08] So we've achieved 2.3 and uh
[00:53:10] dramatically improved on the bigram
[00:53:12] language model using this simple neural
[00:53:14] net as described here
[00:53:16] um using these 3,400 parameters.
[00:53:20] Now there's something we have to be
[00:53:20] careful with.
[00:53:22] I said that we have a better model
[00:53:24] because we are achieving a lower loss,
[00:53:26] 2.3, much lower than 2.45 with the
[00:53:28] bigram model previously.
[00:53:30] Now that's not exactly true. And the
[00:53:32] reason that's not true is that
[00:53:37] this is actually fairly small model, but
[00:53:39] these models can get larger and larger
[00:53:41] if you keep adding neurons and
[00:53:42] parameters. So, you can imagine that we
[00:53:44] don't potentially have a thousand
[00:53:46] parameters. We could have 10,000 or
[00:53:47] 100,000 or millions of parameters.
[00:53:50] And as the capacity of the neural
[00:53:51] network grows,
[00:53:52] it becomes more and more capable of
[00:53:55] overfitting your training set.
[00:53:57] What that means is that the loss on the
[00:53:59] training set, on the data that you're
[00:54:00] training on, will become very, very low,
[00:54:03] as low as zero.
[00:54:04] But all that the model is doing is
[00:54:06] memorizing your training set verbatim.
[00:54:09] So, if you take that model, and it looks
[00:54:10] like it's working really well, but you
[00:54:12] try to sample from it, you will
[00:54:13] basically only get examples exactly as
[00:54:15] they are in the training set. You won't
[00:54:17] get any new data.
[00:54:19] In addition to that, if you try to
[00:54:20] evaluate the loss on some withheld names
[00:54:23] or other words, you will actually see
[00:54:25] that the loss on those can be very high.
[00:54:28] As a basically, it's not a good model.
[00:54:30] So, the standard in the field it is is
[00:54:32] to split up your data set into three
[00:54:34] splits, as we call them. We have the
[00:54:36] training split, the dev split or the
[00:54:38] validation split,
[00:54:40] and the test split.
[00:54:42] So, training split,
[00:54:45] test or um sorry, dev or validation
[00:54:48] split,
[00:54:49] and test split.
[00:54:52] And typically, this would be say 80% of
[00:54:54] your data set, this could be 10% and
[00:54:56] this 10% roughly.
[00:54:58] So, you have these three splits of the
[00:55:00] data.
[00:55:01] Now, these 80% of your training of of
[00:55:03] the data set, the training set, is used
[00:55:05] to optimize the parameters of the model,
[00:55:07] just like we're doing here, using
[00:55:08] gradient descent.
[00:55:10] These 10% of the um examples, the dev or
[00:55:13] validation split, they're used for
[00:55:15] development over all the hyper
[00:55:17] parameters of your model. So, hyper
[00:55:19] parameters are for example, the size of
[00:55:21] this hidden layer,
[00:55:22] the size of the embedding. So, this is a
[00:55:24] hundred or a two for us, but we could
[00:55:26] try different things.
[00:55:28] The strength of the regularization,
[00:55:29] which we aren't using yet so far.
[00:55:32] So, there's lots of different hyper
[00:55:33] parameters and settings that go into
[00:55:34] defining a neural net, and you can try
[00:55:36] many different variations of them and
[00:55:38] see whichever one works best on your
[00:55:41] validation split.
[00:55:43] So, this is used to train the
[00:55:44] parameters.
[00:55:45] This is used to train the hyper
[00:55:47] parameters.
[00:55:48] And test split is used to evaluate uh
[00:55:51] basically the performance of the model
[00:55:53] at the end.
[00:55:54] So, we're only evaluating the loss on
[00:55:55] the test split very, very sparingly and
[00:55:57] very few times because every single time
[00:56:00] you evaluate your test loss and you
[00:56:02] learn something from it,
[00:56:04] you are basically starting to also train
[00:56:06] on the test split. So, you are only
[00:56:09] allowed to test the loss on the test set
[00:56:12] um very, very few times. Otherwise, you
[00:56:15] risk overfitting to it as well as you
[00:56:17] experiment on your model.
[00:56:19] So, let's also split up our training
[00:56:21] data into train, dev, and test. And
[00:56:24] then, we are going to train on train and
[00:56:26] only evaluate on test very, very
[00:56:28] sparingly.
[00:56:29] Okay, so here we go.
[00:56:31] Here is where we took all the words and
[00:56:33] put them into X and Y tensors.
[00:56:36] So, instead, let me create a new cell
[00:56:37] here and let me just copy-paste some
[00:56:39] code here
[00:56:41] because I don't think it's that
[00:56:43] complex, but um
[00:56:45] we're going to try to save a little bit
[00:56:46] of time.
[00:56:47] I'm converting this to be a function
[00:56:49] now. And this function takes some list
[00:56:51] of words and builds the arrays X and Y
[00:56:54] for those words only.
[00:56:56] And then here, I am shuffling up all the
[00:56:59] words. So, these are the input words
[00:57:01] that we get.
[00:57:02] We are randomly shuffling them all up.
[00:57:05] And then, um
[00:57:06] we're going to
[00:57:08] set N1 to be
[00:57:10] the number of examples, that's 80% of
[00:57:11] the words, and N2 to be 90% of the
[00:57:14] weight of the words.
[00:57:16] So, basically, if length of words is
[00:57:18] 30,000, N1 is
[00:57:21] Oh, sorry. I should probably run this.
[00:57:24] N1 is 25,000 and N2 is 28,000.
[00:57:28] And so, here we see that I'm calling
[00:57:30] build data set to build the training set
[00:57:32] X and Y
[00:57:33] by indexing into up to N1. So, we're
[00:57:36] going to have only 25,000 training
[00:57:38] words.
[00:57:39] And then we're going to have um
[00:57:42] roughly
[00:57:44] N2 minus N1
[00:57:46] 3,000 validation examples or dev
[00:57:49] examples. And we're going to have
[00:57:52] um
[00:57:53] len of words basically minus N2
[00:57:57] or 3,204
[00:57:59] examples
[00:58:01] here for the test set.
[00:58:03] So,
[00:58:04] now we have X's and Y's for all those
[00:58:07] three splits.
[00:58:11] Um
[00:58:13] Oh, yeah. I'm printing their size here
[00:58:14] inside the function as well.
[00:58:19] But here we don't have words, but these
[00:58:20] are already the individual examples made
[00:58:22] from those words.
[00:58:25] So, let's now scroll down here.
[00:58:27] And the data set now for training is
[00:58:31] more like this.
[00:58:33] And then when we reset the network,
[00:58:38] when we're training, we're only going to
[00:58:40] be training using X train,
[00:58:43] X train, and Y train.
[00:58:47] So, that's the only thing we're training
[00:58:49] on.
[00:58:57] Let's see where we are on the
[00:59:00] single batch.
[00:59:02] Let's now train maybe a few more steps.
[00:59:08] Training a neural network can take a
[00:59:09] while. Usually, you don't do it in line.
[00:59:11] You launch a bunch of jobs and you wait
[00:59:12] for them to finish.
[00:59:13] Um
[00:59:14] can take in multiple days and so on.
[00:59:16] Luckily, this is a very small network.
[00:59:21] Okay, so the loss is pretty good. Oh, we
[00:59:24] accidentally used a learning rate that
[00:59:25] is way too low.
[00:59:27] So, let me actually come back.
[00:59:29] We use the decay learning rate of 0.01.
[00:59:35] So, this will train much faster.
[00:59:37] And then here, when we evaluate, uh
[00:59:39] let's use the dev set here.
[00:59:42] X dev
[00:59:43] and Y dev to evaluate the loss.
[00:59:47] Okay.
[00:59:48] Uh
[00:59:48] and let's not decay the learning rate
[00:59:50] and only do say 10,000 examples.
[00:59:55] And let's evaluate the dev loss once
[00:59:58] here.
[00:59:59] Okay, so we're getting about 2.3 on dev.
[01:00:01] And so, the neural network when it was
[01:00:02] training did not see these dev examples.
[01:00:05] It hasn't optimized on them. And yet,
[01:00:08] when we evaluate the loss on these dev,
[01:00:10] we actually get a pretty decent loss.
[01:00:12] And so, we can also look at what the
[01:00:16] loss is on all of training set.
[01:00:19] Oops.
[01:00:20] And so, we see that the training and the
[01:00:22] dev loss are about equal. So, we're not
[01:00:24] over- fitting. Um this model is not
[01:00:27] powerful enough to just be purely
[01:00:29] memorizing the data. And so far, we are
[01:00:32] what's called under-fitting because the
[01:00:34] training loss and the dev or test losses
[01:00:36] are roughly equal. So, what that
[01:00:38] typically means is that our network is
[01:00:40] very tiny, very small. And we expect to
[01:00:43] make uh performance improvements by
[01:00:45] scaling up the size of this neural net.
[01:00:47] So, let's do that now. So, let's come
[01:00:49] over here
[01:00:50] and let's increase the size of the
[01:00:51] neural net.
[01:00:52] The easiest way to do this is we can
[01:00:54] come here to the hidden layer, which
[01:00:55] currently has 100 neurons, and let's
[01:00:57] just pump this up. So, let's do 300
[01:00:59] neurons.
[01:01:00] And then, this is also 300 biases. And
[01:01:03] here we have 300 inputs into the final
[01:01:05] layer.
[01:01:07] So,
[01:01:08] let's initialize our neural net. We now
[01:01:10] have 10,000 10,000 parameters instead of
[01:01:13] 3,000 parameters.
[01:01:15] And then, we're not using this.
[01:01:18] And then here, what I'd like to do is
[01:01:19] I'd like to actually uh keep track of uh
[01:01:23] that
[01:01:24] um
[01:01:27] Okay, let's just do this. Let's keep
[01:01:29] stats again.
[01:01:30] And here when we're keeping track of the
[01:01:34] loss, let's just also keep track of the
[01:01:37] steps. And let's just have a eye here.
[01:01:41] And let's train on 30,000.
[01:01:44] Or rather say
[01:01:46] Okay, let's try 30,000.
[01:01:48] And we are at 0.1.
[01:01:51] And
[01:01:52] we should be able to run this.
[01:01:55] And optimize neural net.
[01:01:57] And then here basically I want to
[01:01:59] PLT.plot
[01:02:01] the steps
[01:02:02] against the loss.
[01:02:09] So these are the x's and y's.
[01:02:11] And this is
[01:02:13] the loss function and how it's being
[01:02:15] optimized.
[01:02:16] Now you see that there's quite a bit of
[01:02:18] thickness to this, and that's because we
[01:02:19] are optimizing over these mini batches.
[01:02:21] And the mini batches create a little bit
[01:02:23] of noise in this.
[01:02:25] Uh where are we in the dev set? We are
[01:02:27] at 2.5. So we still haven't optimized
[01:02:30] this neural net very well.
[01:02:32] And that's probably because we made it
[01:02:33] bigger. It might take longer for this
[01:02:34] neural net to converge.
[01:02:36] Um
[01:02:37] and so let's continue training.
[01:02:40] Um
[01:02:42] yeah, let's just continue training.
[01:02:46] One possibility is that the batch size
[01:02:48] is so low
[01:02:49] that we just have way too much noise in
[01:02:51] the training. And we may want to
[01:02:53] increase the batch size so that we have
[01:02:54] a bit more
[01:02:56] correct gradient and we're not thrashing
[01:02:58] too much. And we can actually like
[01:03:00] optimize more properly.
[01:03:08] Okay.
[01:03:08] Uh this will now become meaningless
[01:03:10] because we've reinitialized these. So
[01:03:13] yeah, this looks not pleasing like now.
[01:03:16] But there probably is like a tiny
[01:03:17] improvement, but it's so hard to tell.
[01:03:20] Uh let's go again.
[01:03:22] 2.52
[01:03:25] Let's try to decrease the learning rate
[01:03:27] by a factor of two.
[01:03:50] Okay, we're at 2.32.
[01:03:52] Let's continue training.
[01:04:05] We basically expect to see a lower loss
[01:04:07] than what we had before, because now we
[01:04:09] have a much, much bigger model, and we
[01:04:10] were underfitting. So, we'd expect that
[01:04:12] increasing the size of the model should
[01:04:14] help the neural net.
[01:04:16] 2.32 Okay, so that's not happening too
[01:04:18] well.
[01:04:19] Now, one other concern is that even
[01:04:21] though we've made the tanh layer here,
[01:04:23] uh the hidden layer, much, much bigger,
[01:04:25] it could be that the bottleneck of the
[01:04:26] network right now are these embeddings
[01:04:28] that are two dimensional. It can be that
[01:04:30] we're just cramming way too many
[01:04:32] characters into just two dimensions, and
[01:04:34] the neural net is not able to really use
[01:04:36] that space effectively, and that that is
[01:04:38] sort of like the bottleneck to our
[01:04:39] network's performance.
[01:04:42] Okay, 2.23. So, just by decreasing the
[01:04:45] learning rate, I was able to make quite
[01:04:46] a bit of progress. Let's run this one
[01:04:47] more time.
[01:04:51] And then evaluate the training and the
[01:04:53] dev loss.
[01:04:56] Now, one more thing after training that
[01:04:58] I'd like to do is I'd like to visualize
[01:05:00] the um
[01:05:02] embedding vectors for these um
[01:05:05] characters before we scale up uh the
[01:05:08] embedding size from two.
[01:05:09] Because we'd like to make uh this
[01:05:11] bottleneck potentially go away.
[01:05:13] But once I make this greater than two,
[01:05:15] we won't be able to visualize them.
[01:05:17] So here, okay, we're at 2.23 and 2.24.
[01:05:21] So um
[01:05:22] we're not improving much more, and maybe
[01:05:24] the bottleneck now is the character
[01:05:25] embedding size, which is two.
[01:05:28] So here I have a bunch of code that will
[01:05:29] create a figure,
[01:05:31] and then we're going to visualize
[01:05:34] the embeddings that were trained by the
[01:05:35] neural net
[01:05:36] on these characters. Because right now
[01:05:38] the embedding size is just two, so we
[01:05:40] can visualize all the characters with
[01:05:41] the X and the Y coordinates as the two
[01:05:44] embedding locations for each of these
[01:05:46] characters.
[01:05:47] And so here are the X coordinates and
[01:05:50] the Y coordinates, which are the columns
[01:05:51] of C.
[01:05:52] And then for each one, I also include
[01:05:55] the text of the little character.
[01:05:58] So here what we see is actually kind of
[01:05:59] interesting.
[01:06:01] Um
[01:06:02] the network has basically learned to
[01:06:04] separate out the characters and cluster
[01:06:06] them a little bit. Uh so for example,
[01:06:08] you see how the vowels
[01:06:09] a e i o u are clustered up here.
[01:06:12] So what that's telling us that is that
[01:06:14] the neural net treats these as very
[01:06:15] similar, right? Because when they feed
[01:06:17] into the neural net, the embedding
[01:06:19] uh for all of these characters is very
[01:06:21] similar. And so the neural net thinks
[01:06:23] that they're very similar and kind of
[01:06:24] like interchangeable, if that makes
[01:06:26] sense.
[01:06:27] Um
[01:06:29] then the the points that are like really
[01:06:31] far away are for example Q. Q is kind of
[01:06:33] treated as an exception, and Q has a
[01:06:35] very special embedding vector, so to
[01:06:37] speak.
[01:06:38] Similarly, dot, which is a special
[01:06:40] character, is all the way out here.
[01:06:42] And a lot of the other letters are sort
[01:06:44] of like clustered up here.
[01:06:46] And so it's kind of interesting that
[01:06:47] there's a little bit of structure here
[01:06:49] um after the training,
[01:06:51] and it's not definitely not random, and
[01:06:53] these embeddings make sense.
[01:06:56] So we're now going to scale up the
[01:06:57] embedding size and won't be able to
[01:06:59] visualize it directly, but we expect
[01:07:01] that because we're underfitting,
[01:07:03] and we made this layer much bigger and
[01:07:06] did not sufficiently improve the loss.
[01:07:08] We're thinking that the
[01:07:09] um
[01:07:10] constraint to better performance right
[01:07:12] now could be these embedding vectors.
[01:07:15] So, let's make them bigger. Okay, so
[01:07:16] let's scroll up here.
[01:07:18] And now we don't have two-dimensional
[01:07:19] embeddings, we are going to have
[01:07:21] say 10-dimensional embeddings for each
[01:07:23] word.
[01:07:25] Then
[01:07:26] this layer will receive 3 * 10, so 30
[01:07:30] inputs
[01:07:31] will go into
[01:07:33] um
[01:07:33] the hidden layer.
[01:07:35] Let's also make the hidden layer a bit
[01:07:37] smaller. So, instead of 300, let's just
[01:07:38] do 200 neurons in that hidden layer.
[01:07:41] So, now the total number of elements
[01:07:43] will be slightly bigger at 11,000.
[01:07:47] And then we here we have to be a bit
[01:07:48] careful because um
[01:07:50] okay, the learning rate we set to 0.1.
[01:07:53] Here we are hardcoding six and
[01:07:56] obviously, if you're working in
[01:07:56] production, you don't want to be
[01:07:57] hardcoding magic numbers. But instead of
[01:08:00] six, this should now be 30.
[01:08:02] Um
[01:08:04] and let's run it for 50,000 iterations
[01:08:06] and let me split out the initialization
[01:08:08] here outside
[01:08:10] so that when we run this cell multiple
[01:08:12] times, it's not going to wipe out our
[01:08:14] loss.
[01:08:17] In addition to that,
[01:08:19] here
[01:08:20] let's instead of logging loss.item,
[01:08:22] let's actually uh log the
[01:08:25] let's um do log 10,
[01:08:28] I believe that's a function of the loss.
[01:08:32] And I'll show you why in a second. Let's
[01:08:34] optimize this.
[01:08:37] Basically, I'd like to plot the log loss
[01:08:39] instead of the loss because when you
[01:08:40] plot the loss, many times it can have
[01:08:42] this hockey stick appearance and log
[01:08:44] squashes it in.
[01:08:46] Uh so, it just kind of like looks nicer.
[01:08:49] So, the x-axis is step I
[01:08:51] and the y-axis will be the loss I.
[01:09:00] And then here, this is 30.
[01:09:03] Ideally, we wouldn't be hard coding
[01:09:04] these.
[01:09:08] Okay, so let's look at the loss.
[01:09:11] Okay? It's again very thick because the
[01:09:13] mini batch size is very small, but the
[01:09:15] total loss over the training set is 2.3
[01:09:18] and the the test or the dev set is 2.38
[01:09:20] as well.
[01:09:22] So so far so good. Uh let's try to now
[01:09:24] decrease the learning rate
[01:09:25] by a factor of 10
[01:09:29] and train for another 50,000 iterations.
[01:09:35] We'd hope that we would be able to beat
[01:09:37] uh 2.32.
[01:09:43] But again, we're just kind of like doing
[01:09:44] this very haphazardly, so I don't
[01:09:46] actually have confidence that our
[01:09:48] learning rate is set very well, that our
[01:09:50] learning rate decay, which we just do at
[01:09:53] random, is set very well.
[01:09:55] And um so the optimization here is kind
[01:09:57] of suspect, to be honest, and this is
[01:09:59] not how you would do it typically in
[01:10:00] production. In production, you would
[01:10:02] create parameters or hyper parameters
[01:10:04] out of all these settings, and then you
[01:10:05] would run lots of experiments and see
[01:10:07] whichever ones are working well for you.
[01:10:11] Okay.
[01:10:12] So we have 2.17 now and 2.2. Okay. So
[01:10:16] you see how the training and the
[01:10:18] validation performance are starting to
[01:10:20] slightly slowly depart.
[01:10:23] So maybe we're getting the sense that
[01:10:24] the neural net is getting good enough or
[01:10:28] that number of parameters is large
[01:10:30] enough that we are slowly starting to
[01:10:32] overfit.
[01:10:34] Uh let's maybe run one more iteration of
[01:10:36] this
[01:10:38] and see where we get.
[01:10:41] But yeah, basically, you would be
[01:10:43] running lots of experiments, and then
[01:10:44] you are slowly scrutinizing whichever
[01:10:46] ones give you the best dev performance.
[01:10:48] And then once you find all the uh hyper
[01:10:50] parameters that make your dev
[01:10:51] performance good, you take that model
[01:10:53] and you evaluate the test set
[01:10:55] performance a single time. And that's
[01:10:57] the number that you report in your paper
[01:10:59] or wherever else you want to talk about
[01:11:00] and brag about your model.
[01:11:05] So, let's then rerun the plot and rerun
[01:11:08] the train and dev.
[01:11:11] And because we're getting lower loss
[01:11:12] now, it is the case that the embedding
[01:11:14] size of these was holding us back very
[01:11:17] likely.
[01:11:20] Okay, so 2.16 2.19 is what we're roughly
[01:11:22] getting.
[01:11:24] So, there's many ways to go from many
[01:11:26] ways to go from here. We can continue
[01:11:28] tuning the optimization.
[01:11:30] We can continue, for example, playing
[01:11:32] with the sizes of the neural net. Or we
[01:11:33] can increase the number of um
[01:11:36] words or characters, in our case, that
[01:11:38] we are taking as an input. So, instead
[01:11:39] of just three characters, we could be
[01:11:40] taking more characters than as an input.
[01:11:43] And that could further improve the loss.
[01:11:46] Okay, so I changed the code slightly, so
[01:11:48] we have here 200,000 steps of the
[01:11:50] optimization. And in the first 100,000,
[01:11:52] we're using a learning rate of 0.1. And
[01:11:54] then in the next 100,000, we're using a
[01:11:56] learning rate of 0.01.
[01:11:58] This is the loss that I achieve.
[01:12:00] And these are the performance on the
[01:12:01] training and validation loss.
[01:12:04] And in particular, the best validation
[01:12:05] loss I've been able to obtain in the
[01:12:07] last 30 minutes or so is 2.17.
[01:12:10] So, now I invite you to beat this
[01:12:12] number. And you have quite a few knobs
[01:12:14] available to you to, I think, surpass
[01:12:15] this number.
[01:12:17] So, number one, you can of course change
[01:12:18] the number of neurons in the hidden
[01:12:20] layer of this model.
[01:12:21] You can change the dimensionality of the
[01:12:23] embedding uh lookup table.
[01:12:25] You can change the number of characters
[01:12:26] that are feeding in as an input um as
[01:12:29] the context into this model.
[01:12:32] And then, of course, you can change the
[01:12:33] details of the optimization. How long
[01:12:35] are we running? What is the learning
[01:12:37] rate? How does it change over time?
[01:12:39] Uh how does it decay?
[01:12:41] Uh you can change the batch size, and
[01:12:42] you may be able to actually achieve a
[01:12:44] much better convergence speed in terms
[01:12:46] of uh how many seconds or minutes it
[01:12:48] takes to train the model and uh get uh
[01:12:51] your result in terms of really good um
[01:12:54] loss.
[01:12:55] And then of course, I actually invite
[01:12:57] you to read this paper. It is 19 pages,
[01:12:59] but at this point you should actually be
[01:13:00] able to read a good chunk of this paper
[01:13:03] and understand
[01:13:04] uh pretty good chunks of it.
[01:13:06] And this paper also has quite a few
[01:13:08] ideas for improvements that you can play
[01:13:09] with.
[01:13:11] So, all of those are knobs available to
[01:13:12] you, and you should be able to beat this
[01:13:14] number. I'm leaving that as an exercise
[01:13:16] to the reader, and uh that's it for now,
[01:13:18] and I'll see you next time.
[01:13:24] Before we wrap up, I also wanted to show
[01:13:25] how you would sample from the model.
[01:13:28] So, we're going to generate 20 samples.
[01:13:31] At first, we begin with all dots, so
[01:13:33] that's the context. And then until we
[01:13:36] generate the zeroth character again,
[01:13:40] we're going to embed the current context
[01:13:43] using the embedding table C.
[01:13:46] Now, usually uh here, the first
[01:13:48] dimension was the size of the training
[01:13:50] set, but here we're only working with a
[01:13:51] single example that we're generating, so
[01:13:53] this is just um dimension one, just for
[01:13:55] simplicity.
[01:13:57] Um and so this embedding then gets
[01:14:00] projected into the hidden state. You get
[01:14:02] the logits. Now, we calculate the
[01:14:04] probabilities. For that, you can use
[01:14:06] f.softmax
[01:14:08] um of logits, and that just basically
[01:14:10] exponentiates the logits and makes them
[01:14:12] sum to one.
[01:14:13] And similar to cross entropy, it is
[01:14:15] careful that there's no overflows.
[01:14:18] Once we have the probabilities, we
[01:14:19] sample from them using torch.multinomial
[01:14:22] to get our next index, and then we shift
[01:14:24] the context window to append the index
[01:14:26] and record it.
[01:14:28] And then we can just um decode all the
[01:14:30] integers to strings and print them out.
[01:14:33] And so these are some example samples,
[01:14:35] and you can see that the model now works
[01:14:36] much better. So, the words here are much
[01:14:39] more word-like or name-like. So, we have
[01:14:41] things like ham, um
[01:14:44] joes,
[01:14:46] uh lela,
[01:14:48] you know, it's starting to sound a
[01:14:49] little bit more name-like. So, we're
[01:14:51] definitely making progress, uh, but we
[01:14:52] can still improve on this model quite a
[01:14:54] lot.
[01:14:55] Okay, sorry. There's some bonus content.
[01:14:57] I wanted to mention that I want to make
[01:14:59] these notebooks more accessible. And so,
[01:15:01] I don't want you to have to, like,
[01:15:03] install Jupyter notebooks and torch and
[01:15:04] everything else. So, I will be sharing a
[01:15:06] link to a Google Colab.
[01:15:09] And the Google Colab will look like a
[01:15:10] notebook in your browser. And you can
[01:15:13] just go to a URL, and you'll be able to
[01:15:15] execute all the code that you saw in the
[01:15:17] Google Colab. And so, this is me
[01:15:20] executing the code in this lecture, and
[01:15:22] I shortened it a little bit.
[01:15:23] Uh, but basically, you you're able to
[01:15:25] train the exact same network, and then
[01:15:27] plot and sample from the model, and
[01:15:29] everything is ready for you to, like,
[01:15:30] tinker with the numbers right there in
[01:15:32] your browser. No installation necessary.
[01:15:34] Um, so, I just wanted to point that out,
[01:15:36] and the link to this will be in the
[01:15:37] video description.
