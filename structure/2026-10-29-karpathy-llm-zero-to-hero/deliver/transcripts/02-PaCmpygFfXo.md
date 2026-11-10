# 原始逐字稿 02：The spelled-out intro to language modeling: building makemore

> 来源：https://www.youtube.com/watch?v=PaCmpygFfXo
> 语言：英文；YouTube 自动字幕，非人工逐字校对。仅重排空行与排版，保留非空事件顺序及措辞；不翻译、不修正识别错误。时间戳来自 JSON3。
> 视频时长：01:57:45；字幕末尾起始时间：01:57:44。

[00:00:00] Hi everyone. Hope you're well.
[00:00:02] And uh next up what I'd like to do is
[00:00:03] I'd like to build out make more.
[00:00:06] Like micrograd before it, make more is a
[00:00:08] repository that I have on my GitHub
[00:00:10] webpage. Uh you can look at it. Uh but
[00:00:12] just like with micrograd, I'm going to
[00:00:14] build it out step-by-step and I'm going
[00:00:16] to spell everything out. So, we're going
[00:00:18] to build it out slowly and together.
[00:00:20] Now, what is make more?
[00:00:22] Make more, uh as the name suggests, uh
[00:00:24] makes more of things that you give it.
[00:00:27] So, here's an example. names.txt is an
[00:00:30] example data set to make more.
[00:00:32] And when you look at names.txt, you'll
[00:00:34] find that it's a very large data set of
[00:00:36] names.
[00:00:38] So,
[00:00:40] here's lots of different types of names.
[00:00:41] In fact, I believe there are 32,000
[00:00:43] names that I've sort of found randomly
[00:00:45] on a government website.
[00:00:47] And if you train make more on this data
[00:00:50] set, it will learn to make more of
[00:00:52] things like this. Um and in particular
[00:00:56] in this case, that will mean more things
[00:00:58] that sound name-like, but are actually
[00:01:01] unique names. And maybe if you have a
[00:01:03] baby and you're trying to assign name,
[00:01:05] maybe you're looking for a cool new
[00:01:06] sounding unique name, make more might
[00:01:08] help you.
[00:01:09] So, here are some example generations
[00:01:11] from the neural network once we train it
[00:01:14] on our data set.
[00:01:16] So, here's some example unique names
[00:01:18] that it will generate. Dontal,
[00:01:21] uh Irot,
[00:01:23] uh Zendy,
[00:01:24] and so on.
[00:01:25] And so, all these sort of sound
[00:01:27] name-like, uh but they're not, of
[00:01:28] course, names.
[00:01:30] So, under the hood, make more is a
[00:01:32] character-level language model. So, what
[00:01:35] that means is that it is treating every
[00:01:37] single line here as an example.
[00:01:39] And within each example, it's treating
[00:01:41] them all as sequences of individual
[00:01:44] characters. So, r e e s e is this
[00:01:48] example, and that's the sequence of
[00:01:49] characters, and that's the level on
[00:01:51] which we are building out make more.
[00:01:53] And what it means to to a
[00:01:55] character-level language model then is
[00:01:57] that it's just sort of modeling those
[00:01:59] sequences of characters and it knows how
[00:02:00] to predict the next character in the
[00:02:02] sequence.
[00:02:03] Now, we're actually going to implement a
[00:02:05] large number of character level language
[00:02:07] models in terms of the neural networks
[00:02:09] that are involved in predicting the next
[00:02:10] character in a sequence. So, very simple
[00:02:13] bigram and bag of word models,
[00:02:15] multi-layer perceptrons, recurrent
[00:02:17] neural networks, all the way to modern
[00:02:19] transformers. In fact, the transformer
[00:02:21] that we will build will be basically the
[00:02:23] equivalent transformer to GPT-2 if you
[00:02:26] have heard of GPT. Uh so, that's kind of
[00:02:28] a big deal. It's a modern network and by
[00:02:30] the end of this series you will actually
[00:02:32] understand how that works
[00:02:34] um on the level of characters.
[00:02:36] Now, to give you a sense of the
[00:02:38] extensions here, uh after characters we
[00:02:40] will probably spend some time on the
[00:02:42] word level so that we can generate
[00:02:43] documents of words, not just little, you
[00:02:45] know, segments of characters.
[00:02:47] Uh but we can generate entire large,
[00:02:49] much larger documents.
[00:02:51] And then we're probably going to go into
[00:02:52] images and image text uh networks such
[00:02:55] as DALL-E, Stable Diffusion, and so on.
[00:02:58] But for now we have to start
[00:02:59] uh here, character level language
[00:03:01] modeling. Let's go.
[00:03:03] So, like before we are starting with a
[00:03:04] completely blank Jupyter notebook page.
[00:03:07] The first thing is I would like to
[00:03:08] basically load up the data set
[00:03:10] names.txt.
[00:03:11] So, we're going to open up names.txt for
[00:03:13] reading.
[00:03:15] And we're going to read in everything
[00:03:17] into a massive string.
[00:03:19] And then, because it's a massive string,
[00:03:21] we'd only like the individual words and
[00:03:23] put them in a list.
[00:03:24] So, let's call splitlines on that string
[00:03:27] to get all of our words as a Python list
[00:03:30] of strings.
[00:03:32] So, basically we can look at for example
[00:03:33] the first 10 words
[00:03:35] and we have that it's a list of Emma,
[00:03:39] Olivia, Ava, and so on.
[00:03:41] And if we look at
[00:03:43] the top of the page here, that is indeed
[00:03:45] what we see.
[00:03:47] Um
[00:03:48] So, that's good.
[00:03:49] This list actually makes me feel that
[00:03:52] this is probably sorted by frequency.
[00:03:55] But okay, so these are the words. Now,
[00:03:58] we'd like to actually like learn a
[00:04:00] little bit more about this data set.
[00:04:01] Let's look at the total number of words.
[00:04:03] We expect this to be roughly 32,000.
[00:04:06] And then what is the for example
[00:04:07] shortest word?
[00:04:09] So min of
[00:04:11] len of each word for W in words. So the
[00:04:13] shortest word will be length two.
[00:04:18] And max of len W for W in words. So the
[00:04:21] longest word will be
[00:04:23] 15 characters.
[00:04:24] So let's now think through our very
[00:04:25] first language model.
[00:04:27] As I mentioned, a character-level
[00:04:28] language model is predicting the next
[00:04:30] character in a sequence given already
[00:04:33] some concrete sequence of characters
[00:04:35] before it.
[00:04:36] Now, what we have to realize here is
[00:04:37] that every single word here, like
[00:04:39] Isabella,
[00:04:40] is actually quite a few examples packed
[00:04:43] in to that single word.
[00:04:45] Because what is a an existence of a word
[00:04:47] like Isabella in the data set telling us
[00:04:48] really? It's saying that
[00:04:51] the character I is a very likely
[00:04:53] character to come first in the sequence
[00:04:56] of a name.
[00:04:58] The character S is likely to come
[00:05:01] after I.
[00:05:04] The character A is likely to come after
[00:05:06] IS.
[00:05:07] The character B is very likely to come
[00:05:09] after ISA. And so on all the way to A
[00:05:12] following Isabella.
[00:05:14] And then there's one more example
[00:05:15] actually packed in here.
[00:05:17] And that is that
[00:05:19] after there's Isabella,
[00:05:21] the word is very likely to end.
[00:05:23] So that's one more sort of explicit
[00:05:25] piece of information that we have here.
[00:05:27] That we have to be careful with.
[00:05:29] And so there's a lot packed into a
[00:05:31] single individual word in terms of the
[00:05:33] statistical structure of what's likely
[00:05:35] to follow in these character sequences.
[00:05:38] And then of course we don't have just an
[00:05:39] individual word. We actually have 32,000
[00:05:41] of these. And so there's a lot of
[00:05:42] structure here to model.
[00:05:44] Now, in the beginning what I'd like to
[00:05:46] start with is I would like to start with
[00:05:48] building a bigram language model.
[00:05:51] Now, in a bigram language model, we're
[00:05:53] always working with just two characters
[00:05:55] at a time.
[00:05:56] So, we're only looking at one character
[00:05:59] that we are given, and we're trying to
[00:06:00] predict the next character in the
[00:06:02] sequence.
[00:06:03] So, um what characters are likely to
[00:06:06] follow R? What characters are likely to
[00:06:08] follow A? And so on. And we're just
[00:06:10] modeling that kind of a little local
[00:06:11] structure.
[00:06:13] And we're forgetting the fact that we
[00:06:15] may have a lot more information. We're
[00:06:17] always just looking at the previous
[00:06:18] character to predict the next one. So,
[00:06:20] it's a very simple and weak language
[00:06:21] model, but I think it's a great place to
[00:06:23] start.
[00:06:24] So, now let's begin by looking at these
[00:06:25] bigrams in our data set and what they
[00:06:27] look like. And these bigrams, again, are
[00:06:29] just two characters in a row.
[00:06:31] So, for W words,
[00:06:33] each W here is an individual word
[00:06:35] string.
[00:06:36] We want to iterate uh for
[00:06:39] in We want to iterate this word
[00:06:41] with consecutive characters. So, two
[00:06:44] characters at a time, sliding it through
[00:06:46] the word. Now, a interesting, nice way,
[00:06:49] cute way to do this in Python, by the
[00:06:50] way, is doing something like this. For
[00:06:52] character one, character two in zip off
[00:06:56] W and W at one.
[00:07:00] one colon
[00:07:01] print
[00:07:03] character one, character two
[00:07:04] And let's not do all the words. Let's
[00:07:05] just do the first three words. And I'm
[00:07:07] going to show you in a second how this
[00:07:09] works.
[00:07:10] But for now, basically, as an example,
[00:07:12] let's just do the very first word alone,
[00:07:13] Emma.
[00:07:15] You see how we have a Emma, and this
[00:07:18] will just print EM, MM, MA.
[00:07:21] And the reason this works is because W
[00:07:23] is the string Emma, W at one colon is
[00:07:26] the string MMA,
[00:07:28] and zip takes two iterators, and it
[00:07:32] pairs them up, and then creates an
[00:07:34] iterator over the tuples of their
[00:07:35] consecutive entries.
[00:07:37] And if any one of these lists is shorter
[00:07:39] than the other, then it will just uh
[00:07:41] halt and return.
[00:07:43] So basically, uh that's why we return E
[00:07:46] M M M M M M A,
[00:07:50] but then because this iterator, the
[00:07:51] second one here, runs out of elements,
[00:07:54] zip just ends, and that's why we only
[00:07:56] get these tuples. So, pretty cute.
[00:07:59] So, these are the consecutive elements
[00:08:01] in the first word.
[00:08:03] Now, we have to be careful because we
[00:08:04] actually have more information here than
[00:08:05] just these three examples. As I
[00:08:08] mentioned, we know that E is the is very
[00:08:11] come first, and we know that A in this
[00:08:13] case is coming last.
[00:08:15] So, one way to do this is basically
[00:08:17] we're going to create a special array
[00:08:20] here of characters.
[00:08:23] And
[00:08:24] we're going to hallucinate a special
[00:08:25] start token here.
[00:08:28] I'm going to
[00:08:29] call it like special start.
[00:08:32] So, this is a list of one element plus
[00:08:36] W
[00:08:37] and then plus a special end character.
[00:08:41] And the reason I'm wrapping the list of
[00:08:42] W here is because W is a string in a
[00:08:46] list of W will just have the individual
[00:08:48] characters in the list.
[00:08:50] And then doing this again now, but not
[00:08:54] iterating over Ws but over the
[00:08:56] characters,
[00:08:58] will give us something like this.
[00:09:00] So, E is likely So, this is a bigram of
[00:09:02] the start character and E, and this is a
[00:09:05] bigram of the A and the special end
[00:09:07] character.
[00:09:09] And now we can look at, for example,
[00:09:10] what this looks like for
[00:09:12] Olivia or Ava.
[00:09:14] And indeed, we can actually
[00:09:16] potentially do this for the entire data
[00:09:17] set, but we won't print that. That's
[00:09:19] going to be too much.
[00:09:20] But these are the individual character
[00:09:22] bigrams, and we can print them.
[00:09:25] Now, in order to learn the statistics
[00:09:26] about which characters are likely to
[00:09:28] follow other characters, the simplest
[00:09:30] way in the bigram language models is to
[00:09:32] simply do it by counting.
[00:09:34] So, we're basically just going to count
[00:09:36] how often any one of these combinations
[00:09:38] occurs in the training set.
[00:09:40] In these words. So we're going to need
[00:09:42] some kind of a dictionary that's going
[00:09:44] to maintain some counts for every one of
[00:09:46] these bigrams. So let's use a dictionary
[00:09:48] B.
[00:09:49] And this will map these bigrams. So
[00:09:52] bigram is a tuple of character one
[00:09:54] character two.
[00:09:56] And then B at bigram
[00:09:58] will be B.get of bigram
[00:10:01] which is basically the same as B at
[00:10:03] bigram.
[00:10:04] But in the case that bigram is not in
[00:10:07] the dictionary B, we would like to by
[00:10:09] default return a zero.
[00:10:11] Plus one.
[00:10:13] So this will basically add up all the
[00:10:15] bigrams and count how often they occur.
[00:10:18] Let's get rid of printing.
[00:10:20] Or rather
[00:10:22] let's keep the printing and let's just
[00:10:24] inspect what B is in this case.
[00:10:27] And we see that many bigrams occur just
[00:10:29] a single time. This one allegedly
[00:10:31] occurred three times.
[00:10:33] So A was an ending character three
[00:10:34] times. And that's true for all of these
[00:10:36] words.
[00:10:38] All of Emma, Olivia, and Ava end with A.
[00:10:41] Uh so that's why this occurred three
[00:10:43] times.
[00:10:45] Um
[00:10:46] now let's do it for all the words.
[00:10:51] Oops, I should not have printed.
[00:10:55] I meant to erase that.
[00:10:56] Let's kill this.
[00:10:58] Let's just run.
[00:11:00] And now B will have the statistics of
[00:11:02] the entire data set.
[00:11:04] So these are the counts across all the
[00:11:05] words of the individual bigrams.
[00:11:08] And we could for example look at some of
[00:11:10] the most common ones and least common
[00:11:11] ones.
[00:11:12] Um this kind of grows in Python, but the
[00:11:14] way to do this, the simplest way I like,
[00:11:17] is we just use B.items.
[00:11:19] B.items returns
[00:11:21] the tuples of
[00:11:24] key value. In this case the keys are the
[00:11:27] character bigrams and the values are the
[00:11:29] counts.
[00:11:31] And so then what we want to do is we
[00:11:32] want to do um
[00:11:35] sorted of this.
[00:11:38] Uh but by default sort is on the first
[00:11:41] um
[00:11:43] on the first item of a tuple, but we
[00:11:45] want to sort by the values, which are
[00:11:47] the second element of a tuple, that is
[00:11:49] the key value.
[00:11:50] So we want to use the key
[00:11:53] equals lambda
[00:11:55] uh that takes the key value
[00:11:57] and returns the key value at the at one,
[00:12:01] not at zero, but at one, which is the
[00:12:03] count. So we want to sort by the count
[00:12:07] of these elements.
[00:12:10] And actually we want it to go backwards.
[00:12:12] So here what we have is the bigram QNR
[00:12:16] occurs only a single time.
[00:12:18] Uh DZ occurred only a single time.
[00:12:20] And when we sort this the other way
[00:12:21] around,
[00:12:23] we're going to see the most likely
[00:12:25] bigrams. So we see that N was very often
[00:12:29] an ending character
[00:12:30] many, many times. And apparently N
[00:12:32] almost always follows an A. And that's a
[00:12:34] very likely combination as well.
[00:12:37] Um
[00:12:38] so
[00:12:39] this is kind of the individual counts
[00:12:42] that we achieve over the entire data
[00:12:43] set.
[00:12:45] Now it's actually going to be
[00:12:46] significantly more convenient for us to
[00:12:48] keep this information in a
[00:12:49] two-dimensional array instead of a
[00:12:51] Python dictionary.
[00:12:53] So we're going to store this information
[00:12:56] in a 2D array
[00:12:58] and
[00:13:00] the rows are going to be the first
[00:13:01] character of the bigram and the columns
[00:13:03] are going to be the second character.
[00:13:05] And each entry in this two-dimensional
[00:13:06] array will tell us how often that first
[00:13:08] character follows the second character
[00:13:10] in the data set.
[00:13:12] So in particular, the array
[00:13:14] representation that we're going to use
[00:13:16] or the library is that of PyTorch.
[00:13:18] And PyTorch is a deep learning neural
[00:13:21] network framework, but part of it is
[00:13:23] also this torch.tensor, uh which allows
[00:13:25] us to create multi-dimensional arrays,
[00:13:27] and manipulate them very efficiently.
[00:13:29] So, let's import PyTorch, which you can
[00:13:32] do by import torch.
[00:13:34] And then we can create uh arrays.
[00:13:37] So, let's create a array of zeros.
[00:13:40] And we give it a um size of this array.
[00:13:43] Let's create a 3x5 array as an example.
[00:13:47] And
[00:13:48] this is a 3x5 array of zeros.
[00:13:51] And by default, you'll notice a data D
[00:13:53] type, which is short for data type, is
[00:13:55] float 32. So, these are single-precision
[00:13:57] floating-point numbers.
[00:13:59] Because we are going to represent
[00:14:00] counts, let's actually use D type as
[00:14:03] torch.int32.
[00:14:05] So, these are uh
[00:14:07] 32-bit integers.
[00:14:10] So, now you see that we have integer
[00:14:12] data inside this tensor.
[00:14:14] Now, tensors allow us to really um
[00:14:17] manipulate all the individual entries
[00:14:19] and do it very efficiently.
[00:14:20] So, for example, if we want to change
[00:14:22] this bit, we have to index into the
[00:14:24] tensor. And in particular, here, this is
[00:14:28] the first row, and the um because it's
[00:14:31] zero-indexed. So, this is row index one,
[00:14:35] and column index 0 1 2 3.
[00:14:38] So, A at 1,3, we can set that to 1.
[00:14:43] And then A will have a 1 over there.
[00:14:47] We can of course also do things like
[00:14:48] this. So, now A will be 2 over there.
[00:14:52] Or 3.
[00:14:53] And also, we can for example say A 0 0
[00:14:56] is 5.
[00:14:57] And then A will have a 5 over here.
[00:15:00] So, that's how we can index into the
[00:15:02] arrays. Now, of course, the array that
[00:15:04] we are interested in is much much
[00:15:05] bigger. So, for our purposes, we have 26
[00:15:08] letters of the alphabet, and then we
[00:15:10] have two special characters, S and E.
[00:15:13] So, uh we want 26 + 2 or 28x28 array.
[00:15:19] And let's call it the the N, because
[00:15:21] it's going to represent sort of the
[00:15:22] counts.
[00:15:24] Let me erase this stuff.
[00:15:26] So, that's the array that starts at
[00:15:28] zeros, 28 by 28.
[00:15:30] And now let's copy paste this
[00:15:33] here.
[00:15:34] But instead of having a dictionary be
[00:15:37] which we're going to erase, we now have
[00:15:39] an N.
[00:15:41] Now, the problem here is that we have
[00:15:42] these characters which are strings, but
[00:15:44] we have to now
[00:15:45] um basically index into a um array, and
[00:15:49] we have to index using integers. So, we
[00:15:51] need some kind of a lookup table from
[00:15:53] characters to integers.
[00:15:55] So, let's construct such a character
[00:15:56] array.
[00:15:58] And the way we're going to do this is
[00:15:59] we're going to take all the words, which
[00:16:01] is a list of strings.
[00:16:02] We're going to concatenate all of it
[00:16:04] into a massive string. So, this is just
[00:16:06] simply the entire data set as a single
[00:16:07] string.
[00:16:09] We're going to pass this to the set
[00:16:10] constructor, which takes this massive
[00:16:13] string and throws out duplicates because
[00:16:16] sets do not allow duplicates.
[00:16:18] So, set of this will just be the set of
[00:16:21] all the lowercase characters.
[00:16:24] And there should be a total of 26 of
[00:16:26] them.
[00:16:28] And now we actually don't want a set, we
[00:16:30] want a list.
[00:16:32] But we don't want a list sorted in some
[00:16:34] weird arbitrary way, we want it to be
[00:16:36] sorted
[00:16:37] from A to Z.
[00:16:39] So, a sorted list.
[00:16:41] So, those are our characters.
[00:16:45] Now, what we want is this lookup table
[00:16:47] as I mentioned. So, let's create a
[00:16:49] special S2I, I will call it.
[00:16:53] Um S is string or character, and this
[00:16:55] will be an S2I mapping
[00:16:58] for
[00:17:00] IS in enumerate of these characters.
[00:17:04] So, enumerate basically gives us this
[00:17:06] iterator over the integer index and the
[00:17:10] actual element of the list. And then we
[00:17:12] are mapping the character to the
[00:17:13] integer.
[00:17:15] So, S2I
[00:17:16] is a mapping from A to 0, B to 1, etc.
[00:17:19] All the way from Z to 25.
[00:17:24] And that's going to be useful here, but
[00:17:25] we actually also have to specifically
[00:17:27] set that S will be 26.
[00:17:29] And S 2 I at E
[00:17:32] will be 27, right? Because Z was 25.
[00:17:35] So, those are the lookups. And now we
[00:17:38] can come here and we can map both
[00:17:40] character one and character two to their
[00:17:41] integers.
[00:17:42] So, this will be S 2 I at character one.
[00:17:45] And IX2 will be S 2 I of character two.
[00:17:49] And now we should be able to
[00:17:52] do this line, but using our array. So, N
[00:17:55] at IX1, IX2, this is the two-dimensional
[00:17:58] array indexing I showed you before,
[00:18:00] and honestly just plus equals one.
[00:18:02] Because everything starts at zero.
[00:18:06] So, this should work and give us a large
[00:18:10] 28 by 28 array
[00:18:13] of all these counts. So, if we print N,
[00:18:16] this is the array, but of course it
[00:18:18] looks ugly. So, let's erase this ugly
[00:18:21] mess and let's try to visualize it a bit
[00:18:22] more nicer.
[00:18:24] So, for that we're going to use a
[00:18:26] library called Matplotlib.
[00:18:28] So, Matplotlib allows us to create
[00:18:30] figures. So, we can do things like
[00:18:32] plt.imshow of the counter array.
[00:18:36] So, this is the 28 by 28 array.
[00:18:38] And this is a structure, but even this,
[00:18:41] I would say, is still pretty ugly. So,
[00:18:44] we're going to try to create a much
[00:18:45] nicer visualization of it, and I wrote a
[00:18:47] bunch of code for that.
[00:18:49] Uh, the first thing we're going to need
[00:18:50] is
[00:18:52] we're going to need to invert this array
[00:18:54] here, this um dictionary. So, S 2 I is a
[00:18:57] mapping from S to I.
[00:18:59] And in I 2 S, we're going to reverse
[00:19:02] this dictionary. So, iterate over all
[00:19:03] the items and just reverse that array.
[00:19:06] So, I 2 S maps inversely from 0 to A, 1
[00:19:10] to B, etc.
[00:19:12] So, we'll need that.
[00:19:14] And then here's the code that I came up
[00:19:16] with to try to make this a little bit
[00:19:17] nicer.
[00:19:20] We create a figure.
[00:19:22] We plot N.
[00:19:24] And then we do and then we visualize a
[00:19:26] bunch of things later. Let me just run
[00:19:28] it so you get a sense of what all this
[00:19:29] is.
[00:19:32] Okay.
[00:19:33] So, you see here that we have
[00:19:35] the array spaced out. And every one of
[00:19:38] these is basically like B follows G zero
[00:19:41] times.
[00:19:42] B follows H 41 times. Um so, A follows J
[00:19:46] 175 times.
[00:19:48] And so, what you can see that I'm doing
[00:19:49] here is first I show that entire array.
[00:19:53] And then I iterate over all the
[00:19:54] individual little cells here.
[00:19:56] And I create a character string here.
[00:19:59] Which is the inverse mapping I to S of
[00:20:02] the integer I and the integer J. So,
[00:20:04] that's These are the bigrams in a
[00:20:06] character representation.
[00:20:08] And then I plot just the bigram text.
[00:20:12] And then I plot the number of times that
[00:20:14] this bigram occurs.
[00:20:16] Now, the reason that there's a dot item
[00:20:17] here is because when you index into
[00:20:20] these arrays, these are torch tensors.
[00:20:23] You see that we still get a tensor back.
[00:20:26] So, the type of this thing, you'd think
[00:20:28] it would be just an integer 149, but
[00:20:29] it's actually torch.tensor.
[00:20:32] And so, if you do dot item, then it will
[00:20:34] pop out that individual integer.
[00:20:38] So, it'll just be 149.
[00:20:40] So, that's what's happening there. And
[00:20:42] these are just some options to make it
[00:20:43] look nice.
[00:20:45] So, what is the structure of this array?
[00:20:47] Um
[00:20:49] We have all these counts, and we see
[00:20:50] that some of them occur often and some
[00:20:52] of them do not occur often.
[00:20:54] Now, if you scrutinize this carefully,
[00:20:56] you will notice that we're not actually
[00:20:57] being very clever.
[00:20:58] That's because when you come over here,
[00:21:00] you'll notice that for example, we have
[00:21:02] an entire row of completely zeros. And
[00:21:04] that's because the end character
[00:21:07] is never possibly going to be the first
[00:21:08] character of a bigram because we're
[00:21:10] always placing these end tokens all at
[00:21:12] the end of the bigram.
[00:21:14] Similarly, we have entire columns of
[00:21:16] zeros here because the S
[00:21:19] character will never possibly be the
[00:21:21] second element of a bigram because we
[00:21:23] always start with S and we end with E
[00:21:25] and we only have the words in between.
[00:21:27] So, we have an entire column of zeros,
[00:21:29] an entire row of zeros. And in this
[00:21:32] little 2 by 2 matrix here as well, the
[00:21:34] only one that can possibly happen is if
[00:21:36] S directly follows E.
[00:21:38] That can be non-zero if we have a word
[00:21:41] that has no letters. So, in that case
[00:21:43] there's no letters in the word, it's an
[00:21:44] empty word and we just have S follows E.
[00:21:47] But, the other ones are just not
[00:21:49] possible.
[00:21:50] And so, we're basically wasting space
[00:21:51] and not only that, but the S and the E
[00:21:53] are getting very crowded here.
[00:21:55] I was using these brackets because
[00:21:57] there's convention in natural language
[00:21:58] processing to use these kinds of
[00:22:00] brackets to denote special tokens. Uh
[00:22:03] but, we're going to use something else.
[00:22:05] So, let's fix all of this and make it
[00:22:06] prettier.
[00:22:08] We're not actually going to have two
[00:22:09] special tokens, we're only going to have
[00:22:11] one special token.
[00:22:13] So, we're going to have n by n array of
[00:22:15] 27 by 27 instead.
[00:22:18] Instead of having two, we will just have
[00:22:21] one and I will call it a dot.
[00:22:24] Okay?
[00:22:27] Let me swing this over here.
[00:22:30] Now, one more thing that I would like to
[00:22:31] do is I would actually like to make this
[00:22:33] special character have position zero and
[00:22:36] I would like to offset all the other
[00:22:37] letters off. I find that a little bit
[00:22:39] more pleasing.
[00:22:41] Um
[00:22:42] so,
[00:22:44] we need a plus one here so that the
[00:22:46] first character, which is A, will start
[00:22:48] at one.
[00:22:49] So, S to I will now be A starts at one
[00:22:53] and dot is zero.
[00:22:55] And uh I to S, of course, we're not
[00:22:58] changing this because I to S just
[00:22:59] creates a reverse mapping and this will
[00:23:01] work fine. So, one is A, two is B, zero
[00:23:04] is dot.
[00:23:06] So, we reverse that. Here,
[00:23:09] we have
[00:23:10] a dot and a dot.
[00:23:13] This should work fine.
[00:23:14] Make sure I start at zeros.
[00:23:17] Count. And then here, we don't go up to
[00:23:19] 28, we go up to 27.
[00:23:22] And this should just work.
[00:23:30] Okay.
[00:23:31] So, we see that dot dot never happened.
[00:23:33] It's at zero because we don't have empty
[00:23:35] words.
[00:23:36] Then this row here now is just very
[00:23:38] simply the
[00:23:40] counts for all the first letters. So, G
[00:23:45] J starts a word, H starts a word, I
[00:23:47] starts a word, etc. And then these are
[00:23:50] all the ending
[00:23:51] characters.
[00:23:53] And in between, we have the structure of
[00:23:54] what characters follow each other.
[00:23:57] So, this is the counts array of our
[00:23:59] entire uh data set. So, this array
[00:24:02] actually has all of the information
[00:24:03] necessary for us to actually sample from
[00:24:06] this bigram
[00:24:07] character level language model.
[00:24:09] And
[00:24:10] roughly speaking, what we're going to do
[00:24:12] is we're just going to start following
[00:24:13] these probabilities and these counts,
[00:24:15] and we're going to start sampling from
[00:24:17] the from the model.
[00:24:18] So, in the beginning, of course,
[00:24:20] we start with the dot, the start token.
[00:24:23] Dot. So, to sample the first character
[00:24:26] of a name, we're looking at this row
[00:24:28] here.
[00:24:30] So, we see that we have the counts, and
[00:24:32] those counts are telling are telling us
[00:24:34] how often any one of these characters is
[00:24:37] to start a word.
[00:24:39] So, if we take this N,
[00:24:41] and we grab the first row,
[00:24:44] we can do that by using just indexing at
[00:24:47] zero,
[00:24:48] and then using this notation colon for
[00:24:51] the rest of that row.
[00:24:53] So, N zero colon
[00:24:56] is indexing into the zeroth um row and
[00:24:59] then it's grabbing all the columns.
[00:25:02] And so this will give us a
[00:25:03] one-dimensional array
[00:25:05] of the first row. So 0 4 4 10.
[00:25:08] You know it's 0 4 4 10 1 3 0 6 1 5 4 2
[00:25:12] etc. It's just the first row.
[00:25:14] The shape of this is 27. It's just a row
[00:25:17] of 27.
[00:25:19] And the other way that you can do this
[00:25:21] also is you just you don't need to
[00:25:22] actually give this
[00:25:23] you just uh grab the zeroth row like
[00:25:25] this. This is equivalent.
[00:25:28] Now these are the counts.
[00:25:30] And now what we'd like to do is we'd
[00:25:31] like to basically um sample from this.
[00:25:35] Since these are the raw counts, we
[00:25:36] actually have to convert this to
[00:25:37] probabilities.
[00:25:39] So we create a probability vector.
[00:25:42] So we'll take n of zero
[00:25:45] and we'll actually convert this to float
[00:25:48] first.
[00:25:50] Okay, so these integers are converted to
[00:25:51] float
[00:25:52] a floating point numbers. And the reason
[00:25:54] we're creating floats is because we're
[00:25:56] about to normalize these counts.
[00:25:58] So to create a probability distribution
[00:26:00] here, we want to divide
[00:26:03] we basically want to do p p p divide
[00:26:05] p.sum.
[00:26:09] And now we get a vector of smaller
[00:26:11] numbers and these are now probabilities.
[00:26:13] So of course because we divided by the
[00:26:15] sum, the sum of p now is one.
[00:26:18] So this is a nice proper probability
[00:26:20] distribution. It sums to one and this is
[00:26:22] giving us the probability for any single
[00:26:24] character to be the first uh character
[00:26:26] of a word.
[00:26:28] So now we can try to sample from this
[00:26:29] distribution. To sample from these
[00:26:31] distributions, we're going to use
[00:26:32] torch.multinomial which I've pulled up
[00:26:34] here.
[00:26:36] So torch.multinomial returns uh
[00:26:39] um samples from the multinomial
[00:26:41] probability distribution which is a
[00:26:43] complicated way of saying you give me
[00:26:45] probabilities and I will give you
[00:26:47] integers which are sampled according to
[00:26:49] the probability distribution.
[00:26:51] So this is the signature of the method,
[00:26:53] and to make everything deterministic,
[00:26:54] we're going to use a generator object in
[00:26:57] PyTorch.
[00:26:59] Uh so, this makes everything
[00:27:00] deterministic. So, you when you run this
[00:27:01] on your computer, you're going to the
[00:27:03] exact get the exact same results that
[00:27:04] I'm getting here on my computer.
[00:27:07] So, let me show you how this works.
[00:27:09] Um
[00:27:12] Here's the deterministic way of creating
[00:27:15] a torch generator object,
[00:27:18] seeding it with some number that we can
[00:27:20] agree on.
[00:27:21] So, that seeds a generator, gets gives
[00:27:23] us an object G,
[00:27:25] and then we can pass that G to a
[00:27:27] function
[00:27:28] that creates um
[00:27:30] here random numbers. torch.rand creates
[00:27:32] random numbers, three of them,
[00:27:35] and it's using this generator object to
[00:27:37] as a source of randomness.
[00:27:40] Uh so, uh
[00:27:41] without normalizing it,
[00:27:44] I can just print.
[00:27:46] Uh this is sort of like numbers between
[00:27:48] zero and one that are random according
[00:27:50] to this thing. And whenever I run it
[00:27:52] again,
[00:27:53] I'm always going to get the same result
[00:27:54] because I keep using the same generator
[00:27:56] object, which I'm seeding here.
[00:27:58] And then if I divide
[00:28:01] to normalize, I'm going to get a nice
[00:28:04] probability distribution of just three
[00:28:05] elements.
[00:28:07] And then we can use torch.multinomial to
[00:28:09] draw samples from it. So, this is what
[00:28:11] that looks like.
[00:28:13] torch.multinomial will take
[00:28:16] the torch tensor
[00:28:18] of probability distributions.
[00:28:21] Then we can ask for a number of samples,
[00:28:22] let's say 20.
[00:28:24] replacement equals true means that when
[00:28:27] we draw an element, uh we will uh we can
[00:28:30] draw it, and then we can put it back
[00:28:31] into the list of eligible indices to
[00:28:34] draw again.
[00:28:35] And we have to specify replacement as
[00:28:37] true because by default, uh for for some
[00:28:39] reason, it's false.
[00:28:41] Um and I think,
[00:28:43] you know, it's just something to be
[00:28:44] careful with.
[00:28:45] Uh and the generator is passed in here.
[00:28:47] So, we are going to always get
[00:28:48] deterministic results, the same results.
[00:28:51] So, if I run these two,
[00:28:53] we're going to get a bunch of samples
[00:28:55] from this distribution.
[00:28:57] Now, you'll notice here that the
[00:28:58] probability for the first element in
[00:29:01] this tensor is 60%.
[00:29:04] So, in these 20 samples, we'd expect 60%
[00:29:08] of them to be zero.
[00:29:10] We'd expect 30% of them to be one.
[00:29:14] And because the uh element index two
[00:29:17] has only 10% probability, very few of
[00:29:20] these samples should be two. And indeed,
[00:29:22] we only have a small number of twos.
[00:29:25] And we can sample as many as we would
[00:29:26] like.
[00:29:29] And the more we sample, the more uh
[00:29:31] these numbers should um roughly have the
[00:29:33] distribution here.
[00:29:35] So, we should have lots of zeros, half
[00:29:38] as many um
[00:29:41] ones, and we should have um
[00:29:44] three times as few
[00:29:46] uh sorry, as few ones, and three times
[00:29:48] as few uh
[00:29:50] twos.
[00:29:51] So, you see that we have very few twos,
[00:29:53] we have some ones, and most of them are
[00:29:54] zero. So, that's what torch.multinomial
[00:29:57] is doing.
[00:29:58] For us here,
[00:30:01] we are interested in this row. We've
[00:30:02] created this um
[00:30:05] P here,
[00:30:06] and now we can sample from it.
[00:30:09] So, if we use the same seed,
[00:30:12] and then we sample from this
[00:30:14] distribution, let's just get one sample.
[00:30:18] Then, we see that the sample is, say,
[00:30:20] 13.
[00:30:21] Um so, this will be the index.
[00:30:25] And let's You see how it's a tensor that
[00:30:27] wraps 13. We again have to use that item
[00:30:30] to pop out that integer.
[00:30:32] And now, index would be just the number
[00:30:35] 13.
[00:30:37] And of course, the um we can do we can
[00:30:40] map the I2S of IX to figure out exactly
[00:30:43] which character we're sampling here.
[00:30:46] We're sampling M.
[00:30:48] So, we're saying that the first
[00:30:49] character is M in our generation.
[00:30:53] And just looking at the row here,
[00:30:55] M was drawn and you we can see that M
[00:30:57] actually starts a large number of words.
[00:31:00] M started 2,500 words out of 32,000
[00:31:04] words. So, almost
[00:31:06] a bit less than 10% of the words start
[00:31:08] with M. So, this is actually fairly
[00:31:10] likely character to draw.
[00:31:13] Um
[00:31:15] So, that would be the first character of
[00:31:16] our word and now we can continue to
[00:31:18] sample more characters because now we
[00:31:20] know that M started
[00:31:22] M is already sampled.
[00:31:24] So, now to draw the next character, we
[00:31:26] will come back here and we will look for
[00:31:29] the row
[00:31:30] that starts with M.
[00:31:32] So, you see M
[00:31:34] and we have a row here.
[00:31:36] So, we see that M.
[00:31:38] is
[00:31:39] 516, MA is this many, MB is this many,
[00:31:43] etc. So, these are the counts for the
[00:31:44] next row and that's the next character
[00:31:46] that we are going to now generate. So, I
[00:31:48] think we are ready to actually just
[00:31:50] write out the loop because I think
[00:31:51] you're starting to get a sense of how
[00:31:52] this is going to go.
[00:31:54] The um
[00:31:56] We always begin at index zero because
[00:31:59] that's the start token.
[00:32:02] And then while true,
[00:32:04] we're going to grab the row
[00:32:06] corresponding to index
[00:32:08] that we're currently on. So, that's P.
[00:32:11] So, that's N array at IX.
[00:32:14] Convert it to float is RP.
[00:32:18] Then, we normalize this P to sum to one.
[00:32:25] Accidentally ran the infinite loop.
[00:32:28] We normalize P to sum to one.
[00:32:30] Then we need this generator object
[00:32:33] that we're going to initialize up here
[00:32:35] and we're going to draw a single sample
[00:32:37] from this distribution.
[00:32:40] And then this is going to tell us what
[00:32:42] index is going to be next.
[00:32:46] If the index sampled is zero, then
[00:32:49] that's now the end token.
[00:32:52] So, we will break.
[00:32:55] Otherwise, we are going to print
[00:32:57] s2i of ix.
[00:33:02] i2s of ix.
[00:33:05] And uh that's pretty much it. We're just
[00:33:08] uh this should work.
[00:33:10] Okay, more.
[00:33:12] So, that's the that's the name that
[00:33:13] we've sampled. We started with M. The
[00:33:16] next step was O, then R, and then dot.
[00:33:21] And this dot we printed here as well.
[00:33:24] So,
[00:33:26] let's now do this a few times.
[00:33:28] Um
[00:33:30] So, let's actually create an
[00:33:33] out list here.
[00:33:37] And instead of printing, we're going to
[00:33:38] append. So, out.append this character.
[00:33:44] And then here, let's just print it at
[00:33:46] the end. So, let's just join up all the
[00:33:48] outs, and we're just going to print
[00:33:50] more.
[00:33:51] Okay? Now, we're always getting the same
[00:33:53] result because of the generator.
[00:33:55] So, if you want to do this a few times,
[00:33:56] we can go for I in range
[00:34:00] 10. We can sample 10 names.
[00:34:02] And we can just do that 10 times.
[00:34:05] And these are the names that we're
[00:34:06] getting out.
[00:34:08] Let's do 20.
[00:34:14] I'll be honest with you, this doesn't
[00:34:15] look right.
[00:34:16] So, I stared at it a few minutes to
[00:34:17] convince myself that it actually is
[00:34:19] right.
[00:34:20] The reason these samples are so terrible
[00:34:22] is that bigram language model
[00:34:24] is actually like just like really
[00:34:26] terrible.
[00:34:27] We can generate a few more here.
[00:34:30] And you can see that they're kind of
[00:34:31] like their name-like a little bit, like
[00:34:33] Keanu, O'Reilly, etc. Uh but they're
[00:34:35] just like totally messed up. Um
[00:34:38] And I mean, the reason that this is so
[00:34:40] bad, like we're generating H as a name.
[00:34:43] But you have to think through it from
[00:34:45] the model's eyes. It doesn't know that
[00:34:47] this H is the very first H. All it knows
[00:34:50] is that H was previously, and now how
[00:34:52] likely is H the last character? Well,
[00:34:55] it's somewhat likely, and so it just
[00:34:58] makes it last character. It doesn't know
[00:34:59] that there were other things before it
[00:35:01] or there were not other things before
[00:35:03] it. And so, that's why it's generating
[00:35:05] all these like sun- nonsense names.
[00:35:08] Another way to do this is
[00:35:12] to convince yourself that this is
[00:35:13] actually doing something reasonable even
[00:35:14] though it's so terrible is
[00:35:17] these little piece here are 27, right?
[00:35:20] Like 27.
[00:35:23] So, how about if we did something like
[00:35:24] this?
[00:35:26] Instead of P having any structure
[00:35:27] whatsoever,
[00:35:28] how about if P was just a torch.ones of
[00:35:31] 27?
[00:35:34] of 27.
[00:35:37] By default, this is a float 32, so this
[00:35:39] is fine. Divide 27.
[00:35:42] So, what I'm doing here is this is the
[00:35:45] uniform distribution, which will make
[00:35:47] everything equally likely.
[00:35:49] And we can sample from that. So, let's
[00:35:52] see if that does any better.
[00:35:54] Okay? So, it's This is what you have
[00:35:56] from a model that is completely
[00:35:58] untrained, where everything is equally
[00:35:59] likely. So, it's obviously garbage. And
[00:36:02] then if we have a trained model, which
[00:36:04] is trained on just bigrams,
[00:36:07] this is what we get. So, you can see
[00:36:08] that it is more name-like. It is
[00:36:10] actually working. It's just um
[00:36:14] bigram is so terrible, and we have to do
[00:36:15] better. Now, next I would like to fix an
[00:36:17] inefficiency that we have going on here.
[00:36:20] Because what we're doing here is we're
[00:36:21] always fetching a row of N from the
[00:36:24] counts matrix up ahead.
[00:36:26] And we we're always doing the same
[00:36:27] things. We're converting to float and
[00:36:29] we're dividing and we're doing this
[00:36:30] every single iteration of this loop and
[00:36:32] we just keep re-normalizing these rows
[00:36:34] over and over again and it's extremely
[00:36:35] inefficient and wasteful.
[00:36:37] So, what I'd like to do is I'd like to
[00:36:38] actually prepare a matrix capital P that
[00:36:41] will just have the probabilities in it.
[00:36:43] So, in other words, it's going to be the
[00:36:45] same as the capital N matrix here of
[00:36:47] counts, but every single row will have
[00:36:49] the row of probabilities uh that is
[00:36:51] normalized to one indicating the
[00:36:53] probability distribution for the next
[00:36:55] character given the character before it.
[00:36:58] Um as defined by which row we're in.
[00:37:01] So, basically what we'd like to do is
[00:37:03] we'd like to just do it up front here
[00:37:05] and then we would like to just use that
[00:37:06] row here.
[00:37:07] Uh so, here we would like to just do P
[00:37:10] equals P of IX instead.
[00:37:12] Okay.
[00:37:14] The other reason I want to do this is
[00:37:16] not just for efficiency, but also I
[00:37:17] would like us to practice uh these
[00:37:19] N-dimensional tensors and I'd like us to
[00:37:21] practice uh their manipulation and
[00:37:23] especially something that's called
[00:37:24] broadcasting that we'll go into in a
[00:37:25] second.
[00:37:27] We're actually going to have to become
[00:37:28] very good at these tensor manipulations
[00:37:30] because if we're going to build out all
[00:37:32] the way to transformers, we're going to
[00:37:33] be doing some pretty complicated um
[00:37:35] array operations for efficiency and uh
[00:37:37] we need to really understand that and be
[00:37:39] very good at it.
[00:37:42] So, intuitively what we want to do is we
[00:37:43] first want to grab the floating point
[00:37:45] copy of N.
[00:37:48] And I'm mimicking the line here
[00:37:49] basically.
[00:37:50] And then we want to divide all the rows
[00:37:53] so that they sum to one.
[00:37:55] So, we'd like to do something like this.
[00:37:57] P divide P.sum.
[00:38:00] But, now we have to be careful
[00:38:02] because P.sum actually
[00:38:05] produces a sum
[00:38:08] Sorry. P equals N.float.copy.
[00:38:10] P.sum produces a um
[00:38:14] sums up all of the counts of this entire
[00:38:17] matrix N
[00:38:18] and gives us a single number of just the
[00:38:19] summation of everything. So, that's not
[00:38:21] the way we want to defi- divide. We want
[00:38:23] to simultaneously and in parallel divide
[00:38:26] all the rows by their respective sums.
[00:38:30] So, what we have to do now is we have to
[00:38:32] go into documentation for torch.sum.
[00:38:35] And we can scroll down here to a
[00:38:37] definition that is relevant to us, which
[00:38:38] is where we don't only provide an input
[00:38:41] array that we want to sum, but we also
[00:38:43] provide the dimension along which we
[00:38:45] want to sum.
[00:38:47] And in particular, we want to sum up uh
[00:38:49] over rows, right?
[00:38:52] Now, one more argument that I want you
[00:38:53] to pay attention to here is the keepdim
[00:38:56] is false.
[00:38:57] If keepdim is true, then the output
[00:39:00] tensor is of the same size as input,
[00:39:02] except of course the dimension along
[00:39:03] which you summed, which will become just
[00:39:05] one.
[00:39:07] But, if you pass in uh keepdim as false,
[00:39:12] then this dimension is squeezed out. And
[00:39:14] so, torch.sum not only does the sum and
[00:39:16] collapses dimension to be of size one,
[00:39:18] but in addition, it does what's called a
[00:39:20] squeeze, where it squeeze out it
[00:39:22] squeezes out that dimension.
[00:39:24] So,
[00:39:25] basically what we want here is we
[00:39:27] instead want to do p.sum of sum axis.
[00:39:30] And in particular, notice that p.shape
[00:39:33] is 27 by 27.
[00:39:35] So, when we sum up across axis zero,
[00:39:37] then we would be taking the zeroth
[00:39:39] dimension, and we would be summing
[00:39:40] across it.
[00:39:42] So, when keepdim is true,
[00:39:45] then this thing will not only give us
[00:39:46] the counts across um
[00:39:50] along the columns,
[00:39:52] but notice that basically the shape of
[00:39:53] this is 1 by 27. We just get a row
[00:39:56] vector.
[00:39:57] And the reason we get a row vector here
[00:39:59] again is because we pass in zero
[00:40:00] dimension, so this zero dimension
[00:40:02] becomes one, and we've done a sum,
[00:40:04] and we get a row. And so, basically,
[00:40:06] we've done the sum
[00:40:08] this way,
[00:40:09] vertically, and arrived at just a single
[00:40:11] 1 by 27
[00:40:12] vector of counts.
[00:40:15] What happens when you take out keepdim
[00:40:17] is that we just get 27. So, it squeezes
[00:40:20] out that dimension and we just get um
[00:40:23] a one-dimensional vector of size 27.
[00:40:28] Now, we don't actually want
[00:40:31] 1 by 27 row vector because that gives us
[00:40:33] the counts or the sums across um
[00:40:37] the uh columns.
[00:40:39] We actually want to sum the other way
[00:40:41] along dimension one.
[00:40:42] And you'll see that the shape of this is
[00:40:44] 27 by one. So, it's a column vector.
[00:40:47] It's a 27 by one
[00:40:49] vector of counts.
[00:40:52] Okay?
[00:40:53] And that's because what's happened here
[00:40:55] is that we're going horizontally and
[00:40:57] this 27 by 27 matrix becomes a 27 by one
[00:41:01] array.
[00:41:03] Now, you'll notice by the way that um
[00:41:06] the actual numbers
[00:41:08] of these counts are identical.
[00:41:10] And that's because this special array of
[00:41:12] counts here comes from bigram
[00:41:14] statistics. And actually, it just so
[00:41:15] happens by chance or because of the way
[00:41:18] this array is constructed that the sums
[00:41:20] along the columns or along the rows,
[00:41:23] horizontally or vertically, is
[00:41:24] identical.
[00:41:26] But actually, what we want to do in this
[00:41:27] case is we want to sum across the uh
[00:41:30] rows
[00:41:31] horizontally. So, what we want here is
[00:41:33] p.sum of one with keep dim true.
[00:41:37] 27 by one column vector.
[00:41:39] And now, what we want to do is we want
[00:41:40] to divide by that.
[00:41:44] Now, we have to be careful here again.
[00:41:46] Is it possible to take
[00:41:48] what's a um p.shape you see here is 27
[00:41:51] by 27. Is it possible to take a 27 by 27
[00:41:55] array and divide it by what is a 27 by
[00:41:58] one array?
[00:42:01] Is that an operation that you can do?
[00:42:03] And whether or not you can perform this
[00:42:05] operation is determined by what's called
[00:42:06] broadcasting rules. So, if you just
[00:42:08] search broadcasting semantics in torch,
[00:42:12] you'll notice that there's a special
[00:42:13] definition for uh what's called
[00:42:14] broadcasting that for whether or not
[00:42:18] these two arrays can be combined in a
[00:42:21] binary operation like division.
[00:42:24] So the first condition is each tensor
[00:42:25] has at least one dimension, which is the
[00:42:27] case for us.
[00:42:28] And then when iterating over the
[00:42:29] dimension sizes starting at the trailing
[00:42:31] dimension,
[00:42:32] the dimension sizes must either be
[00:42:33] equal, one of them is one, or one of
[00:42:35] them does not exist.
[00:42:38] Okay? So, let's do that. We need to
[00:42:40] align the two arrays and their shapes,
[00:42:44] which is very easy because both of these
[00:42:45] shapes have two elements, so they're
[00:42:46] aligned.
[00:42:48] Then we iterate over from the from the
[00:42:50] right and going to the left.
[00:42:52] Each dimension must be either equal, one
[00:42:55] of them is a one, or one of them does
[00:42:56] not exist.
[00:42:58] So in this case they're not equal, but
[00:42:59] one of them is a one. So, this is fine.
[00:43:02] And then this dimension, they're both
[00:43:03] equal. So, this is fine.
[00:43:05] So, all the dimensions are fine and
[00:43:08] therefore the this operation is
[00:43:10] broadcastable.
[00:43:12] So that means that this operation is
[00:43:13] allowed.
[00:43:14] And what is it that these arrays do when
[00:43:16] you divide 27 by 27 by 27 by one?
[00:43:19] What it does is that it takes this
[00:43:21] dimension one and it stretches it out.
[00:43:24] It copies it
[00:43:25] to match 27 here in this case.
[00:43:29] So in our case, it takes this column
[00:43:30] vector which is 27 by one
[00:43:32] and it copies it 27 times
[00:43:36] to make
[00:43:37] these both be 27 by 27 internally. You
[00:43:40] can think that way. And so it copies
[00:43:42] those counts
[00:43:44] and then it does an element-wise
[00:43:45] division,
[00:43:47] which is what we want because these
[00:43:48] counts we want to divide by them on
[00:43:50] every single one of these columns in
[00:43:53] this matrix.
[00:43:54] So this actually we expect will
[00:43:56] normalize every single row.
[00:43:59] And we can check that this is true by
[00:44:01] taking the first row for example and
[00:44:04] taking its sum. We expect this to be
[00:44:06] one.
[00:44:08] Because it's now normalized.
[00:44:10] And then we expect this now, because if
[00:44:13] we actually correctly normalize all the
[00:44:14] rows, we expect to get the exact same
[00:44:16] result here. So, let's run this.
[00:44:19] It's the exact same result.
[00:44:21] So, this is correct. So, now I would
[00:44:23] like to scare you a little bit. Uh you
[00:44:25] actually have to like I basically
[00:44:27] encourage you very strongly to read
[00:44:28] through broadcasting semantics.
[00:44:30] And I encourage you to treat this with
[00:44:31] respect. And it's not something to play
[00:44:34] fast and loose with. It's something to
[00:44:35] really respect, really understand, and
[00:44:37] look up maybe some tutorials for
[00:44:39] broadcasting and practice it, and be
[00:44:40] careful with it because you can very
[00:44:42] quickly run into bugs. Let me show you
[00:44:44] what I mean.
[00:44:47] You see how here we have p.sum of one,
[00:44:49] keep dims is true.
[00:44:50] The shape of this is 27 by one.
[00:44:53] Let me take out this line just so we
[00:44:54] have the n, and then we can see the
[00:44:57] counts.
[00:44:58] We can see that this is all the counts
[00:45:00] across all the
[00:45:02] rows.
[00:45:03] And it's a 27 by one column vector,
[00:45:05] right?
[00:45:07] Now, suppose that I tried to do the
[00:45:09] following,
[00:45:10] but I erase keep dims is true here.
[00:45:14] What does that do? If keep dims is not
[00:45:15] true, it's false, then remember,
[00:45:17] according to documentation, it gets rid
[00:45:19] of this dimension one. It squeezes it
[00:45:22] out. So, basically we just get all the
[00:45:24] same counts, the same result, except the
[00:45:27] shape of it is not 27 by one, it is just
[00:45:29] 27. The one disappears.
[00:45:31] But all the counts are the same.
[00:45:34] So, you think that this divide that
[00:45:37] would would work.
[00:45:40] First of all, can we even write this?
[00:45:42] And will it Is it even Is it even
[00:45:44] expected to run? Is it broadcastable?
[00:45:46] Let's determine if this result is
[00:45:47] broadcastable.
[00:45:49] p.sum at one is shape
[00:45:51] is 27.
[00:45:53] This is 27 by 27. So, 27 by 27
[00:45:57] broadcasting into 27.
[00:46:00] So, now
[00:46:01] rules of broadcasting, number one align
[00:46:03] all the dimensions on the right done now
[00:46:06] iteration over all the dimensions
[00:46:07] starting from the right going to the
[00:46:09] left
[00:46:10] all the dimensions must either be equal
[00:46:13] one of them must be one or one of them
[00:46:14] does not exist so here they are all
[00:46:16] equal here the dimension does not exist
[00:46:20] so internally what broadcasting will do
[00:46:21] is it will create a one here
[00:46:24] and then
[00:46:25] we see that one of them is a one and
[00:46:27] this will get copied and this will run
[00:46:30] this will broadcast
[00:46:32] okay so you'd expect this to work
[00:46:37] because we we are
[00:46:41] this broadcasting this we can divide
[00:46:42] this
[00:46:43] now if I run this you'd expect it to
[00:46:45] work but
[00:46:46] it doesn't
[00:46:48] you actually get garbage you get a wrong
[00:46:49] result because this is actually a bug
[00:46:52] this keep them equals true
[00:46:57] makes it work
[00:47:00] this is a bug in
[00:47:03] both cases we are doing the correct
[00:47:05] counts we are summing up across the rows
[00:47:09] but keep them is saving us and making it
[00:47:10] work so in this case
[00:47:12] I'd like you to encourage you to
[00:47:13] potentially like pause this video at
[00:47:15] this point and try to think about why
[00:47:17] this is buggy and why the keep them was
[00:47:19] necessary here
[00:47:22] okay
[00:47:23] so the reason to do
[00:47:24] for this is I'm trying to hint it here
[00:47:26] when I was sort of giving you a bit of a
[00:47:27] hint on how this works
[00:47:29] this
[00:47:30] 27 vector
[00:47:32] internally inside the broadcasting this
[00:47:34] becomes a one by 27
[00:47:36] and one by 27 is a row vector right and
[00:47:39] now we are dividing 27 by 27 by one by
[00:47:42] 27
[00:47:43] and torch will replicate this dimension
[00:47:45] so basically
[00:47:47] it will take
[00:47:49] it will take this
[00:47:51] row vector and it will copy it
[00:47:53] vertically now
[00:47:55] 27 times so the 27 by 27 lines exactly,
[00:47:58] and element twice divides.
[00:48:00] And so, basically, what's happening here
[00:48:02] is
[00:48:03] um
[00:48:04] we're actually normalizing the columns
[00:48:06] instead of normalizing the rows.
[00:48:09] So, you can check that what's happening
[00:48:11] here is that P at zero, which is the
[00:48:13] first row of P, dot sum is not one, it's
[00:48:17] seven.
[00:48:18] It is the first column, as an example,
[00:48:20] that sums to one.
[00:48:23] So,
[00:48:24] to summarize, where does the issue come
[00:48:26] from? The issue comes from the silent
[00:48:28] adding of a dimension here because in
[00:48:30] broadcasting rules, you align on the
[00:48:31] right and go from right to left, and if
[00:48:34] dimension doesn't exist, you create it.
[00:48:36] So, that's where the problem happens. We
[00:48:38] still did the counts correctly. We did
[00:48:39] the counts across the rows, and we got
[00:48:41] the the counts on the right here as a
[00:48:44] column vector. But, because the keepdims
[00:48:46] was true, this this uh this dimension
[00:48:48] was discarded, and now we just have a
[00:48:50] vector 27.
[00:48:51] And because of broadcasting the way it
[00:48:53] works, this vector of 27 suddenly
[00:48:55] becomes a row vector.
[00:48:57] And then this row vector gets replicated
[00:48:58] vertically, and then every single point
[00:49:01] we are dividing by the by the count
[00:49:05] uh in the opposite direction.
[00:49:07] So, uh
[00:49:08] so, this thing just uh doesn't work. You
[00:49:11] This needs to be keepdims equals true in
[00:49:13] this case.
[00:49:14] So, then
[00:49:15] um then we have that P at zero is
[00:49:17] normalized.
[00:49:19] And conversely, the first column, you'd
[00:49:21] expect to potentially not be normalized.
[00:49:24] And this is what makes that work.
[00:49:27] So, pretty subtle, and uh hopefully this
[00:49:31] helps to scare you that you should have
[00:49:33] a respect for broadcasting, be careful,
[00:49:35] check your work,
[00:49:36] uh and uh understand how it works under
[00:49:38] the hood, and make sure that it's
[00:49:39] broadcasting in the direction that you
[00:49:40] like. Otherwise, you're going to
[00:49:41] introduce very subtle bugs, very hard to
[00:49:43] hard to find bugs, and uh just be
[00:49:46] careful. One more note on efficiency, we
[00:49:48] don't want to be doing this here because
[00:49:50] uh this creates a completely new tensor
[00:49:52] that we store into P. We prefer to use
[00:49:55] in-place operations if possible.
[00:49:57] Also, this would be an in-place
[00:49:59] operation. It has the potential to be
[00:50:01] faster. It doesn't create new memory
[00:50:03] under the hood. And then let's erase
[00:50:05] this. We don't need it.
[00:50:07] And let's also
[00:50:10] um just do fewer just so I'm not wasting
[00:50:13] space.
[00:50:14] Okay, so we're actually in a pretty good
[00:50:15] spot now.
[00:50:17] We trained a bigram language model, and
[00:50:19] we trained it really just by counting
[00:50:21] uh how frequently any pairing occurs and
[00:50:24] then normalizing so that we get a nice
[00:50:26] probability distribution.
[00:50:28] So really these elements of this array P
[00:50:31] are really the parameters of our bigram
[00:50:32] language model giving us and summarizing
[00:50:34] the statistics of these bigrams.
[00:50:37] So we trained the model and then we know
[00:50:38] how to sample from the model. We just
[00:50:40] iteratively uh sample the next character
[00:50:43] and uh feed it in each time and get the
[00:50:45] next character.
[00:50:47] Now what I'd like to do is I'd like to
[00:50:48] somehow evaluate the quality of this
[00:50:50] model.
[00:50:51] We'd like to somehow summarize the
[00:50:53] quality of this model into a single
[00:50:54] number. How good is it at predicting uh
[00:50:57] the training set?
[00:50:59] And as an example, so in the training
[00:51:00] set we can evaluate now the training
[00:51:03] loss. And this training loss is telling
[00:51:05] us about uh sort of the quality of this
[00:51:07] model in a single number just like we
[00:51:09] saw in micrograd.
[00:51:11] So let's try to think through the
[00:51:13] quality of the model and how we would
[00:51:14] evaluate it.
[00:51:17] Basically what we're going to do is
[00:51:18] we're going to copy paste this code
[00:51:20] that we previously used for counting.
[00:51:23] Okay?
[00:51:24] And let me just print the bigrams first.
[00:51:26] We're going to use F-strings.
[00:51:27] And I'm going to print character one
[00:51:29] followed by character two. These are the
[00:51:31] bigrams. And then I don't want to do it
[00:51:32] for all the words. Let's just do the
[00:51:34] first three words.
[00:51:36] So here we have Emma, Olivia, and Ava
[00:51:38] bigrams.
[00:51:40] Now what we'd like to do is we'd like to
[00:51:41] basically look at the probability that
[00:51:44] the model assigns to every one of these
[00:51:46] bigrams.
[00:51:48] So, in other words, we can look at the
[00:51:49] probability, which is summarized in the
[00:51:51] matrix P,
[00:51:53] of IX1 IX2.
[00:51:56] And then we can print it here as
[00:51:58] probability.
[00:52:00] And because these probabilities are way
[00:52:01] too large, let me percent uh
[00:52:04] or colon point four F
[00:52:06] to like truncate it a bit.
[00:52:09] So, what do we have here, right? We're
[00:52:10] looking at the probabilities that the
[00:52:11] model assigns to every one of these
[00:52:13] bigrams in the data set.
[00:52:15] And so, we can see some of them are 4%,
[00:52:17] 3%, etc. Just to have a measuring stick
[00:52:19] in our mind, by the way, um
[00:52:21] with 27 possible characters or tokens,
[00:52:24] and if everything was equally likely,
[00:52:26] then you'd expect all these
[00:52:27] probabilities to be
[00:52:30] 4% roughly.
[00:52:32] So, anything above 4% means that we've
[00:52:34] learned something useful from these
[00:52:36] bigram statistics.
[00:52:37] And you see that roughly some of these
[00:52:38] are 4%, but some of them are as high as
[00:52:40] 40%,
[00:52:41] 35%, and so on. So, you see that the
[00:52:44] model actually assigned a pretty high
[00:52:45] probability to whatever's in the
[00:52:47] training set. And so, that that's a good
[00:52:49] thing.
[00:52:50] Um basically, if you have a very good
[00:52:51] model, you'd expect that these
[00:52:53] probabilities should be near one,
[00:52:54] because that means that uh your model is
[00:52:56] correctly predicting what's going to
[00:52:57] come next, especially in the training
[00:52:59] set, where you where you trained your
[00:53:01] model.
[00:53:02] So, now we'd like to think about how can
[00:53:05] we summarize these probabilities into a
[00:53:07] single number that measures the quality
[00:53:09] of this model.
[00:53:11] Now, when you look at the literature
[00:53:13] into maximum likelihood estimation and
[00:53:15] statistical modeling and so on,
[00:53:17] you'll see that what's typically used
[00:53:18] here is something called the likelihood.
[00:53:21] And the likelihood is the product of all
[00:53:23] of these probabilities.
[00:53:25] And so, the product of all of these
[00:53:27] probabilities is the likelihood, and
[00:53:29] it's really telling us about the
[00:53:31] probability of the entire data set
[00:53:33] assigned uh assigned by the model that
[00:53:36] we've trained. And that is a measure of
[00:53:38] quality.
[00:53:39] So, the product of these should be as
[00:53:41] high as possible
[00:53:43] when you are training the model and when
[00:53:44] you have a good model, your your product
[00:53:46] of these probabilities should be very
[00:53:48] high.
[00:53:49] Um
[00:53:50] Now, because the product of these
[00:53:51] probabilities is an unwieldy thing to
[00:53:53] work with, uh you can see that all of
[00:53:55] them are between 0 and 1. So, your
[00:53:56] product of these probabilities will be a
[00:53:58] very tiny number.
[00:54:00] Um so, for convenience, what people work
[00:54:03] with usually is not the likelihood, but
[00:54:04] they work with what's called the log
[00:54:06] likelihood.
[00:54:07] So,
[00:54:09] the product of these is likelihood.
[00:54:10] To get likelihood, we just have to take
[00:54:13] the log of the probability.
[00:54:15] And so, the log of the probability here,
[00:54:17] I have a log of X from 0 to 1.
[00:54:19] The log is a you see here monotonic
[00:54:21] transformation of the probability,
[00:54:24] where if you pass in 1, you get 0.
[00:54:28] So, probability 1 gets you log
[00:54:30] probability of 0.
[00:54:32] And then, as you go lower and lower
[00:54:33] probability, the log will grow more and
[00:54:35] more negative until all the way to
[00:54:37] negative infinity at 0.
[00:54:41] So, here we have a log prob, which is
[00:54:44] really just a torch. log of probability.
[00:54:46] Let's print it out to get a sense of
[00:54:48] what that looks like.
[00:54:50] Log prob,
[00:54:51] also point four if.
[00:54:54] Okay.
[00:54:56] So, as you can see, when we plug in
[00:54:58] numbers that are very close, some of our
[00:55:00] higher numbers, we get closer and closer
[00:55:02] to 0.
[00:55:03] And then, if we plug in very bad
[00:55:05] probabilities, we get more and more
[00:55:06] negative number. That's bad.
[00:55:09] So,
[00:55:10] and the reason we work with this is for
[00:55:13] large extent convenience, right? Because
[00:55:15] we have mathematically that if you have
[00:55:17] some product A * B * C of all these
[00:55:19] probabilities, right? Or the likelihood
[00:55:22] is the product of all these
[00:55:23] probabilities,
[00:55:25] then the log
[00:55:27] of these is just log of A plus log of B
[00:55:33] plus log of C. If you remember your logs
[00:55:36] from your
[00:55:37] high school or undergrad and so on.
[00:55:39] So we have that basically
[00:55:41] the likelihood is the product of
[00:55:42] probabilities, the log likelihood is
[00:55:44] just the sum of the logs of the
[00:55:46] individual probabilities.
[00:55:48] So
[00:55:49] log likelihood
[00:55:52] starts at zero.
[00:55:54] And then log likelihood here we can just
[00:55:57] accumulate simply.
[00:56:00] And in the end we can print this.
[00:56:05] Print the log likelihood.
[00:56:09] F strings.
[00:56:11] Maybe you're familiar with this.
[00:56:13] So log likelihood is -38.
[00:56:19] Okay.
[00:56:21] Now
[00:56:22] we actually want um
[00:56:25] So how high can log likelihood get? It
[00:56:27] can go to zero. So when all the
[00:56:30] probabilities are one, log likelihood
[00:56:31] will be zero. And then when all the
[00:56:33] probabilities are lower, this will grow
[00:56:35] more and more negative.
[00:56:37] Now we don't actually like this because
[00:56:39] what we'd like is a loss function. And a
[00:56:41] loss function has the semantics that low
[00:56:44] is good. Because we're trying to
[00:56:46] minimize the loss. So we actually need
[00:56:49] to invert this. And that's what gives us
[00:56:51] something called the negative log
[00:56:53] likelihood.
[00:56:54] Um
[00:56:55] negative log likelihood is just negative
[00:56:58] of the log likelihood.
[00:57:03] These are F strings by the way if you'd
[00:57:05] like to look this up.
[00:57:06] Negative log likelihood equals
[00:57:09] So negative log likelihood now is just
[00:57:10] the negative of it.
[00:57:12] And so the negative log likelihood is a
[00:57:13] very nice loss function because um
[00:57:17] the lowest it can get is zero. And the
[00:57:20] higher it is, the worse off the
[00:57:22] predictions are that you're making.
[00:57:24] And then one more modification to this
[00:57:26] that sometimes people do is that for
[00:57:27] convenience uh they actually like to
[00:57:29] normalize by they like to make it an
[00:57:32] average instead of a sum.
[00:57:34] And so here
[00:57:37] let's just keep some counts as well.
[00:57:39] So n plus equals one starts at zero. And
[00:57:42] then here we can have sort of like a
[00:57:45] normalized log likelihood.
[00:57:47] Um
[00:57:50] if we just normalize it by the count
[00:57:52] then we will sort of get the average log
[00:57:54] likelihood. So this would be usually our
[00:57:57] loss function here.
[00:57:58] This this we would this is what we would
[00:58:00] use.
[00:58:02] Uh so our loss function for the training
[00:58:03] set assigned by the model is 2.4. That's
[00:58:06] the quality of this model.
[00:58:08] And the lower it is, the better off we
[00:58:10] are. And the higher it is, the worse off
[00:58:12] we are.
[00:58:13] And the job of our, you know, training
[00:58:16] is to find the parameters that minimize
[00:58:19] the negative log likelihood loss.
[00:58:22] And that would be like a high quality
[00:58:24] model. Okay, so to summarize I actually
[00:58:26] wrote it out here.
[00:58:28] So our goal is to maximize likelihood
[00:58:30] which is the product of all the
[00:58:32] probabilities assigned by the model.
[00:58:35] And we want to maximize this likelihood
[00:58:37] with respect to the model parameters.
[00:58:39] And in our case, the model parameters
[00:58:41] here are defined in the table. These
[00:58:43] numbers, the probabilities
[00:58:45] are
[00:58:46] uh the model parameters sort of in our
[00:58:47] bigram language model so far.
[00:58:50] Uh but you have to keep in mind that
[00:58:51] here we are storing everything in a
[00:58:52] table format, the probabilities. But
[00:58:54] what's coming up as a brief preview is
[00:58:57] that these numbers will not be kept
[00:58:59] explicitly but these numbers will be
[00:59:01] calculated by a neural network.
[00:59:03] So that's coming up.
[00:59:04] And we want to change and tune the
[00:59:06] parameters of these neural networks. We
[00:59:08] want to change these parameters to
[00:59:09] maximize the likelihood, the product of
[00:59:11] the probabilities.
[00:59:13] Now maximizing the likelihood is
[00:59:15] equivalent to maximizing the log
[00:59:16] likelihood because log is a monotonic
[00:59:18] function.
[00:59:19] Here's the graph of log.
[00:59:22] And basically all it is doing is it's uh
[00:59:24] just a scaling your um you can look at
[00:59:27] it as just a scaling of the loss
[00:59:28] function.
[00:59:29] And so the optimization problem here and
[00:59:32] here are actually equivalent because
[00:59:34] this is just a scaling. You can look at
[00:59:35] it that way.
[00:59:37] And so these are two identical
[00:59:38] optimization problems.
[00:59:41] Um
[00:59:41] maximizing the log likelihood is
[00:59:43] equivalent to minimizing the negative
[00:59:44] log likelihood.
[00:59:46] And then in practice people actually
[00:59:47] minimize the average negative log
[00:59:49] likelihood to get numbers like 2.4.
[00:59:53] And then this summarizes the quality of
[00:59:55] your model.
[00:59:56] And we'd like to minimize it and make it
[00:59:57] as small as possible.
[00:59:59] And the lowest it can get is zero.
[01:00:02] And the lower it is
[01:00:04] the better off your model is because
[01:00:06] it's assigning it's assigning high
[01:00:07] probabilities to your data.
[01:00:09] Now let's estimate the probability over
[01:00:10] the entire training set just to make
[01:00:12] sure that we get something around 2.4.
[01:00:15] Let's run this over the entire oops.
[01:00:17] Let's take out the print statement as
[01:00:18] well.
[01:00:20] Okay, 2.45 over the entire training set.
[01:00:24] Now what I'd like to show you is that
[01:00:25] you can actually evaluate the
[01:00:26] probability for any word that you want.
[01:00:28] Like for example
[01:00:30] if we just test a single word Andre and
[01:00:32] bring back the print statement
[01:00:35] then you see that Andre is actually kind
[01:00:37] of like an unlikely word. Like on
[01:00:39] average
[01:00:40] um we take three log probability to
[01:00:43] represent it. And roughly that's because
[01:00:45] EJ apparently is very uncommon as an
[01:00:47] example.
[01:00:50] Now
[01:00:51] think through this um
[01:00:53] when I take Andre and I append Q and I
[01:00:55] test the probability of it Andre Q
[01:01:00] we actually get um infinity.
[01:01:03] And that's because JQ has a 0%
[01:01:05] probability according to our model. So
[01:01:07] the log likelihood
[01:01:09] so the log of zero will be negative
[01:01:11] infinity. We get infinite loss.
[01:01:14] So this is kind of undesirable, right?
[01:01:15] Because we plugged in a string that
[01:01:16] could be like a somewhat reasonable
[01:01:18] name. But basically what this is saying
[01:01:20] is that this model is exactly 0% likely
[01:01:23] to uh to predict this name
[01:01:26] and our loss is infinity on this
[01:01:28] example.
[01:01:29] And really what the reason for that is
[01:01:31] that J
[01:01:32] is followed by Q
[01:01:35] uh zero times. Uh where is Q? JQ is zero
[01:01:39] and so JQ is 0% likely.
[01:01:42] So it's actually kind of gross and
[01:01:43] people don't like this too much. To fix
[01:01:45] this, there's a very simple fix that
[01:01:47] people like to do to sort of like smooth
[01:01:49] out your model a little bit that is
[01:01:50] called model smoothing.
[01:01:52] And roughly what's happening is that we
[01:01:53] will we will add some fake counts.
[01:01:56] So imagine adding a count of one to
[01:01:59] everything.
[01:02:00] So we add a count of one
[01:02:03] like this
[01:02:04] and then we recalculate the
[01:02:05] probabilities.
[01:02:07] And that's model smoothing and you can
[01:02:09] add as much as you like. You can add
[01:02:10] five and that will give you a smoother
[01:02:11] model.
[01:02:12] And the more you add here
[01:02:14] the more uniform model you're going to
[01:02:16] have. And the less you add,
[01:02:19] um the more more peaked model you're
[01:02:21] going to have, of course.
[01:02:22] So one is like a pretty decent count to
[01:02:24] add and that will ensure that there will
[01:02:27] be no zeros in our probability matrix P.
[01:02:30] And so this will of course change the
[01:02:32] generations a little bit. In this case
[01:02:34] it didn't but it in principle it could.
[01:02:36] But what that's going to do now is that
[01:02:38] nothing will be infinity unlikely.
[01:02:41] So now
[01:02:42] our model will predict some other
[01:02:44] probability and we see that JQ now has a
[01:02:46] very small probability. So the model
[01:02:48] still finds it very surprising that this
[01:02:49] was a word or bigram but we don't get
[01:02:52] negative infinity.
[01:02:53] So it's kind of like a nice fix that
[01:02:54] people like to apply sometimes and it's
[01:02:55] called model smoothing. Okay, so we've
[01:02:57] now trained a respectable bigram
[01:03:00] character level language model and we
[01:03:01] saw that we both
[01:03:04] a sort of trained the model by looking
[01:03:05] at the counts of all the bigrams and
[01:03:08] normalizing the rows to get probability
[01:03:10] distributions.
[01:03:11] We saw that we can also then use those
[01:03:14] parameters of this model to perform
[01:03:16] sampling of new words.
[01:03:19] So, we sample new names according to
[01:03:21] those distributions. And we also saw
[01:03:22] that we can evaluate the quality of this
[01:03:24] model.
[01:03:25] And the quality of this model is
[01:03:26] summarized in a single number, which is
[01:03:28] the negative log likelihood. And the
[01:03:30] lower this number is, the better the
[01:03:32] model is
[01:03:33] because it is giving high probabilities
[01:03:35] to the actual next characters in all the
[01:03:37] bigrams in our training set.
[01:03:40] So, that's all well and good. But we've
[01:03:42] arrived at this model explicitly by
[01:03:44] doing something that felt sensible. We
[01:03:46] were just performing counts, and then we
[01:03:48] were normalizing those counts.
[01:03:51] Now, what I would like to do is I would
[01:03:52] like to take an alternative approach. We
[01:03:54] will end up in a very, very similar
[01:03:55] position, but the approach will look
[01:03:57] very different because I would like to
[01:03:58] cast the problem of bigram character
[01:04:00] level language modeling into the neural
[01:04:02] network framework.
[01:04:04] And in the neural network framework,
[01:04:05] we're going to approach things slightly
[01:04:07] differently, but again, end up in a very
[01:04:09] similar spot. I'll go into that later.
[01:04:12] Now, our neural network is going to be a
[01:04:15] still a bigram character level language
[01:04:16] model. So, it receives a single
[01:04:18] character as an input.
[01:04:20] Then there's neural network with some
[01:04:21] weights or some parameters W.
[01:04:24] And it's going to output the probability
[01:04:26] distribution over the next character in
[01:04:28] a sequence. It's going to make guesses
[01:04:30] as to what is likely to follow this
[01:04:32] character that was input to the model.
[01:04:36] And then in addition to that, we're
[01:04:37] going to be able to evaluate any setting
[01:04:39] of the parameters of the neural net
[01:04:41] because we have the loss function.
[01:04:43] The negative log likelihood. So, we're
[01:04:45] going to take a look at these
[01:04:46] probability distributions, and we're
[01:04:47] going to use the labels
[01:04:49] which are basically just the identity of
[01:04:51] the next character in that bigram, the
[01:04:53] second character.
[01:04:54] So, knowing what second character
[01:04:56] actually comes next in the bigram allows
[01:04:58] us to then look at what how high of a
[01:05:00] probability the model assigns to that
[01:05:02] character.
[01:05:03] And then we of course want the
[01:05:05] probability to be very high.
[01:05:07] And that is another way of saying that
[01:05:08] the loss is low.
[01:05:10] So, we're going to use gradient-based
[01:05:12] optimization then to tune the parameters
[01:05:14] of this network because we have the loss
[01:05:16] function and we're going to minimize it.
[01:05:18] So, we're going to tune the weights so
[01:05:20] that the neural net is correctly
[01:05:21] predicting the probabilities for the
[01:05:23] next character.
[01:05:24] So, let's get started. The first thing I
[01:05:26] want to do is I want to compile the
[01:05:27] training set of this neural network,
[01:05:29] right? So, create
[01:05:31] the training set
[01:05:33] of all the bigrams.
[01:05:36] Okay?
[01:05:37] And
[01:05:39] here
[01:05:40] I'm going to copy-paste this code
[01:05:43] because this code iterates over all the
[01:05:45] bigrams.
[01:05:47] So, here we start with the words. We
[01:05:49] iterate over all the bigrams. And
[01:05:50] previously, as you recall, we did the
[01:05:52] counts. But now we're not going to do
[01:05:54] counts. We're just creating a training
[01:05:55] set.
[01:05:56] Now, this training set will be made up
[01:05:58] of two lists.
[01:06:02] We have the
[01:06:04] inputs
[01:06:06] and the targets, the the labels.
[01:06:09] And these bigrams will denote XY. Those
[01:06:11] are the characters, right?
[01:06:13] And so, we're given the first character
[01:06:14] of the bigram and then we're trying to
[01:06:16] predict the next one.
[01:06:17] Both of these are going to be integers.
[01:06:19] So, here we'll take X's. data.append is
[01:06:22] just
[01:06:23] X1. Y's.data.append IX2.
[01:06:27] And then here
[01:06:29] we actually don't want lists of
[01:06:30] integers. We will create uh tensors out
[01:06:33] of these. So, X's is torch.tensor
[01:06:36] X's and Y's is torch.tensor of Y's.
[01:06:41] And then we don't actually want to take
[01:06:43] all the words just yet because I want
[01:06:45] everything to be manageable. Uh so,
[01:06:47] let's just do the first word, which is
[01:06:48] Emma.
[01:06:51] And then it's clear what these X's and
[01:06:52] Y's would be.
[01:06:55] Here, let me print
[01:06:57] character one, character two, just so
[01:06:59] you see what's going on here.
[01:07:01] So, the bigrams of these characters is
[01:07:04] .e, em, mm, ma, a. So, so this single
[01:07:09] word, as I mentioned, has 1 2 3 4 5
[01:07:12] examples for our neural network.
[01:07:14] There are five separate examples in
[01:07:16] Emma.
[01:07:17] And those examples are summarized here.
[01:07:19] When the input to the neural neural
[01:07:20] network is integer zero,
[01:07:23] the desired label is integer five, which
[01:07:26] corresponds to e.
[01:07:28] When the input to the neural network is
[01:07:29] five, we want its weights to be arranged
[01:07:32] so that 13 gets a very high probability.
[01:07:35] When 13 is put in, we want 13 to have a
[01:07:37] high probability.
[01:07:39] When 13 is put in, we also want one to
[01:07:41] have a high probability.
[01:07:43] When one is input, we want zero to have
[01:07:45] a very high probability. So, there are
[01:07:47] five separate input examples to a neural
[01:07:50] net
[01:07:51] in this data set.
[01:07:55] I wanted to add a tangent of a note of
[01:07:57] caution to be careful with a lot of the
[01:07:59] APIs of some of these frameworks.
[01:08:01] You saw me silently use torch.Tensor
[01:08:04] with a lowercase t, and the output
[01:08:06] looked right.
[01:08:07] But, you should be aware that there's
[01:08:09] actually two ways of constructing a
[01:08:10] tensor. There's a torch.lowercase
[01:08:13] tensor, and there's also a torch.capital
[01:08:15] tensor class, which you can also
[01:08:17] construct. Uh so, you can actually call
[01:08:19] both. You can also do torch.capital
[01:08:21] tensor,
[01:08:22] and you get an x's and y's as well.
[01:08:25] So, that's not confusing at all.
[01:08:27] Um
[01:08:29] There are threads on what is the
[01:08:29] difference between these two.
[01:08:31] And um
[01:08:33] unfortunately, the docs are just like
[01:08:34] not clear on the difference. And when
[01:08:36] you look at the the docs of lowercase
[01:08:38] tensor, constructs tensor with no
[01:08:40] autograd history by copying data.
[01:08:43] It's just like it doesn't
[01:08:45] it doesn't make sense. So, the actual
[01:08:47] difference, as far as I can tell, is
[01:08:48] explained eventually in this random
[01:08:50] thread that you can Google.
[01:08:51] And really, it comes down to, I believe,
[01:08:55] that um
[01:08:56] where is this?
[01:08:58] torch.Tensor infers the dtype, the data
[01:09:00] type, automatically, while torch.Tensor
[01:09:02] just returns a float tensor.
[01:09:04] I would recommend stick to torch.lower
[01:09:06] case tensor.
[01:09:07] So, um
[01:09:09] indeed, we see that when I construct
[01:09:12] this with a capital T, the data type
[01:09:14] here of X's is float 32.
[01:09:18] But, torch.lower case tensor
[01:09:21] you see how it's now X.dtype is now
[01:09:24] integer.
[01:09:26] So, um
[01:09:28] it's advised that you use lower case T
[01:09:30] and you can read more about it if you
[01:09:32] like in some of these threads.
[01:09:34] Uh but basically
[01:09:35] um
[01:09:36] I'm pointing out some of these things
[01:09:37] beca- because I want to caution you and
[01:09:39] I want you to re- get used to reading a
[01:09:41] lot of documentation and reading through
[01:09:43] a lot of uh Q&A's and threads like this.
[01:09:46] And um
[01:09:48] you know, some of this stuff is
[01:09:49] unfortunately not easy and not very well
[01:09:50] documented and you have to be careful
[01:09:51] out there. What we want here is integers
[01:09:54] because that's what makes uh sense. Um
[01:09:58] and so uh lower case tensor is what we
[01:10:00] are using. Okay, now we want to think
[01:10:02] through how we're going to feed in these
[01:10:03] examples into a neural network.
[01:10:06] Now, it's not quite as straightforward
[01:10:07] as n-
[01:10:09] plugging it in because these examples
[01:10:11] right now are integers. So, there's like
[01:10:12] a 0, 5, or 13. It gives us the index of
[01:10:15] the character and you can't just plug an
[01:10:17] integer index into a neural net.
[01:10:20] These neural nets uh right are sort of
[01:10:22] made up of these neurons.
[01:10:24] And uh these neurons have weights. And
[01:10:27] as you saw in micrograd, these weights
[01:10:29] act multiplicatively on the inputs. WX
[01:10:31] plus B, there's tanh's and so on. And
[01:10:34] so, it doesn't really make sense to make
[01:10:35] an input neuron take on integer values
[01:10:37] that you feed in and then multiply on
[01:10:40] with weights.
[01:10:41] So, instead, a common way of encoding
[01:10:44] integers is what's called one-hot
[01:10:45] encoding.
[01:10:47] In one-hot encoding, uh we take an
[01:10:49] integer like 13 and we create a vector
[01:10:52] that is all zeros except for the 13th
[01:10:54] dimension, which we turn to a one.
[01:10:57] And then that vector can feed into a
[01:10:59] neural net.
[01:11:01] Now, conveniently,
[01:11:03] uh PyTorch actually has something called
[01:11:04] the one-hot uh uh
[01:11:07] um
[01:11:07] function inside torch.nn.functional.
[01:11:10] It takes a tensor made up of integers.
[01:11:13] Um
[01:11:14] long is a is a is an integer.
[01:11:18] Um
[01:11:19] and it also takes a number of classes,
[01:11:21] um
[01:11:22] which is how large you want your uh
[01:11:24] tensor uh your vector to be.
[01:11:27] So here, let's import is a common way of
[01:11:30] importing it.
[01:11:34] And then let's do F.one_hot.
[01:11:36] And we feed in uh the integers that we
[01:11:38] want to encode.
[01:11:40] So we can actually feed in the entire
[01:11:41] array of X's.
[01:11:44] And we can tell it that num_classes is
[01:11:46] 27.
[01:11:47] So it doesn't have to try to guess it.
[01:11:49] It may have guessed that it's only 13
[01:11:51] and would give us an incorrect result.
[01:11:54] So this is the one-hot. Let's call this
[01:11:56] X_enc for X encoded.
[01:12:02] And then we see that X_encoded.shape is
[01:12:04] 5 by 27.
[01:12:07] And uh
[01:12:08] we can also visualize it, plt.imshow of
[01:12:10] X_enc,
[01:12:12] to make it a little bit more clear
[01:12:13] because this is a little messy.
[01:12:15] So we see that we've encoded all the
[01:12:17] five examples uh into vectors.
[01:12:20] We have five examples, so we have five
[01:12:22] rows, and each row here is now an
[01:12:24] example into a neural net.
[01:12:26] And we see that the appropriate bit is
[01:12:28] turned on as a one, and everything else
[01:12:30] is zero.
[01:12:31] So um
[01:12:33] here for example, the the zeroth bit is
[01:12:35] turned on, the fifth bit is turned on,
[01:12:38] 13th bits are turned on for both of
[01:12:40] these examples, and then the first bit
[01:12:42] here is turned on.
[01:12:44] So that's how we can encode um integers
[01:12:47] into vectors.
[01:12:49] And then these vectors can feed in to
[01:12:51] neural nets. One more issue to be
[01:12:52] careful with here, by the way, is
[01:12:55] let's look at the data type of X
[01:12:56] encoding. We always want to be careful
[01:12:58] with data types.
[01:12:59] What would you expect X encoding's data
[01:13:01] type to be? When we're plugging numbers
[01:13:03] into neural nets, we don't want them to
[01:13:05] be integers. We want them to be floating
[01:13:07] point numbers that can take on various
[01:13:09] values. But the D type here is actually
[01:13:12] 64-bit integer.
[01:13:14] And the reason for that, I suspect, is
[01:13:15] that one hot received a 64-bit integer
[01:13:18] here and it returned to the same data
[01:13:21] type.
[01:13:21] And when you look at the signature of
[01:13:23] one hot, it doesn't even take a D type,
[01:13:25] a desired data type of the output
[01:13:27] tensor.
[01:13:28] And so we can't In a lot of functions in
[01:13:30] torch, we'd be able to do something like
[01:13:32] D type equals torch.float32,
[01:13:34] which is what we want, but one hot does
[01:13:36] not support that.
[01:13:37] So instead, we're going to want to cast
[01:13:39] this to float like this.
[01:13:43] So that these
[01:13:44] everything is the same.
[01:13:46] Everything looks the same, but the D
[01:13:48] type is float 32. And floats can feed
[01:13:51] into um neural nets. So now let's
[01:13:53] construct our first neuron.
[01:13:56] This neuron will look at these input
[01:13:58] vectors.
[01:14:00] And as you remember from micrograd,
[01:14:02] these neurons basically perform a very
[01:14:03] simple function, wx plus b, where wx is
[01:14:06] a dot product, right?
[01:14:09] So we can achieve the same thing here.
[01:14:12] Let's first define the weights of this
[01:14:14] neuron. Basically, where are the initial
[01:14:15] weights at initialization for this
[01:14:17] neuron?
[01:14:18] Let's initialize them with torch.randn.
[01:14:21] torch.randn
[01:14:23] is um
[01:14:24] fills a tensor with random numbers
[01:14:27] drawn from a normal distribution.
[01:14:29] And a normal distribution has a
[01:14:32] probability uh density function like
[01:14:33] this. And so most of the numbers drawn
[01:14:35] from this distribution will be around
[01:14:37] zero,
[01:14:38] uh but some of them will be as high as
[01:14:40] almost three and so on. And very few
[01:14:42] numbers will be above three in
[01:14:44] magnitude.
[01:14:46] So we need to take a size as an input
[01:14:49] here.
[01:14:50] And I'm going to use size as 27 by 1.
[01:14:54] So, 27 by 1, and then let's visualize W.
[01:14:58] So, W is a column vector of 27 numbers.
[01:15:03] And uh these weights are then multiplied
[01:15:06] by the inputs.
[01:15:08] So, now to perform this multiplication,
[01:15:10] we can take X encoding
[01:15:12] and we can multiply it with W.
[01:15:15] This is a matrix multiplication operator
[01:15:17] in PyTorch.
[01:15:20] And the output of this operation is 5 by
[01:15:22] 1.
[01:15:23] The reason it's 5 by 1 is the following.
[01:15:25] We took X encoding, which is 5 by 27,
[01:15:29] and we multiplied it by 27 by 1.
[01:15:33] And
[01:15:34] in matrix multiplication,
[01:15:36] you see that the output will become 5 by
[01:15:39] 1 because these 27 will multiply and
[01:15:43] add.
[01:15:44] So, basically what we're seeing here,
[01:15:46] out out of this operation,
[01:15:48] is we are seeing the five um
[01:15:51] activations
[01:15:53] of this neuron
[01:15:56] on these five inputs. And we've
[01:15:58] evaluated all of them in parallel. We
[01:16:00] didn't feed in just a single input to
[01:16:02] this single neuron. We fed in
[01:16:04] simultaneously all the five inputs into
[01:16:06] the same neuron,
[01:16:08] and in parallel, PyTorch has evaluated
[01:16:11] the WX plus B, but here it's just WX.
[01:16:14] There's no bias.
[01:16:15] It has valued W W times X for all of
[01:16:18] them uh independently. Now, instead of a
[01:16:21] single neuron though, I would like to
[01:16:22] have 27 neurons, and I'll show you in a
[01:16:24] second why I want 27 neurons.
[01:16:27] So, instead of having just a one here,
[01:16:29] which is indicating this presence of one
[01:16:31] single neuron,
[01:16:32] we can use 27.
[01:16:34] And then when W is 27 by 27,
[01:16:38] this will in parallel evaluate all the
[01:16:41] 27 neurons on all the five inputs.
[01:16:46] Giving us a much better, much much
[01:16:48] bigger result.
[01:16:49] So, now what we've done is 5 by 27
[01:16:51] multiplied 27 by 27.
[01:16:54] And the output of this is now 5 by 27.
[01:16:57] So, we can see that the shape of this
[01:17:01] is 5 by 27.
[01:17:04] So, what is every element here telling
[01:17:05] us, right?
[01:17:07] It's telling us for every one of 27
[01:17:09] neurons that we created,
[01:17:13] what is the firing rate of those neurons
[01:17:16] on every one of those five examples?
[01:17:19] So,
[01:17:20] the element, for example, 3 {comma} 13
[01:17:25] is giving us the firing rate of the 13th
[01:17:28] neuron looking at the third input.
[01:17:31] And the way this was achieved is by a
[01:17:34] dot product
[01:17:36] between the third input
[01:17:38] and the 13th column
[01:17:41] of this W matrix here.
[01:17:44] Okay? So, using matrix multiplication,
[01:17:47] we can very efficiently evaluate
[01:17:50] the dot product between lots of input
[01:17:52] examples in a batch.
[01:17:55] And lots of neurons, where all of those
[01:17:57] neurons have weights in the columns of
[01:17:59] those Ws.
[01:18:01] And in matrix multiplication, we're just
[01:18:02] doing those dot products and
[01:18:04] in parallel. Just to show you that this
[01:18:06] is the case, we can take X and we can
[01:18:08] take the third
[01:18:10] row.
[01:18:12] And we can take the W and take its 13th
[01:18:14] column.
[01:18:17] And then we can do X and get three.
[01:18:21] Element-wise multiply with W at 13.
[01:18:26] And sum that up. That's WX plus B.
[01:18:29] Uh well, there's no plus B. It's just WX
[01:18:31] dot product. And that's
[01:18:34] this number.
[01:18:35] So, you see that this is just being done
[01:18:36] efficiently by the matrix multiplication
[01:18:39] operation for all the input examples and
[01:18:42] for all the output neurons of this first
[01:18:45] layer.
[01:18:46] Okay, so we fed our 27-dimensional
[01:18:48] inputs into a first layer of a neural
[01:18:50] net that has 27 neurons, right? So, we
[01:18:53] have 27 inputs and now we have 27
[01:18:56] neurons. These neurons perform W * X.
[01:18:59] They don't have a bias and they don't
[01:19:01] have a non-linearity like tanh. We're
[01:19:03] going to leave them to be a linear
[01:19:05] layer.
[01:19:06] In addition to that, we're not going to
[01:19:08] have any other layers. This is going to
[01:19:09] be it. It's just going to be
[01:19:11] the dumbest, smallest, simplest neural
[01:19:13] net, which is just a single linear
[01:19:14] layer.
[01:19:16] And now I'd like to explain what I want
[01:19:18] those 27 outputs to be.
[01:19:21] Intuitively, what we're trying to
[01:19:22] produce here for every single input
[01:19:23] example is we're trying to produce some
[01:19:25] kind of a probability distribution for
[01:19:27] the next character in a sequence. And
[01:19:29] there's 27 of them.
[01:19:31] But we have to come up with like precise
[01:19:33] semantics for exactly how we're going to
[01:19:34] interpret these 27 numbers that these
[01:19:37] neurons take on.
[01:19:39] Now, intuitively,
[01:19:41] you see here that these numbers are
[01:19:42] negative and some of them are positive,
[01:19:44] etc.
[01:19:45] And that's because these are coming out
[01:19:46] of a neural net layer initialized with
[01:19:48] these um
[01:19:50] uh normal distribution
[01:19:52] uh parameters.
[01:19:54] But what we want is we want something
[01:19:55] like we had here. Like each row here
[01:19:59] told us the counts and then we
[01:20:01] normalized the counts to get
[01:20:02] probabilities. And we want something
[01:20:04] similar to come out of a neural net.
[01:20:06] But what we just have right now is just
[01:20:07] some negative and positive numbers.
[01:20:10] Now, we want those numbers to somehow
[01:20:12] represent the probabilities for the next
[01:20:14] character.
[01:20:15] But you see that probabilities, they
[01:20:17] they have a special structure. They um
[01:20:20] they're positive numbers and they sum to
[01:20:21] one.
[01:20:22] And so, that doesn't just come out of a
[01:20:24] neural net.
[01:20:25] And then, they can't be counts because
[01:20:28] uh these counts are positive and counts
[01:20:31] are integers.
[01:20:32] So, counts are also not really a good
[01:20:34] thing to output from a neural net.
[01:20:36] So, instead what the neural net is going
[01:20:38] to output and how we are going to
[01:20:39] interpret the
[01:20:42] the 27 numbers is that these 27 numbers
[01:20:45] are giving us log counts
[01:20:48] basically.
[01:20:49] Um so, instead of giving us counts
[01:20:52] directly like in this table, they're
[01:20:54] giving us log counts.
[01:20:56] And to get the counts, we're going to
[01:20:57] take the log counts and we're going to
[01:20:59] exponentiate them.
[01:21:01] Now,
[01:21:02] exponentiation
[01:21:04] takes the following form.
[01:21:06] Um it takes numbers
[01:21:08] that are negative or they are positive.
[01:21:10] It takes the entire real line. And then
[01:21:13] if you plug in negative numbers, you're
[01:21:14] going to get e to the x, which is
[01:21:18] uh always below one.
[01:21:20] So, you're getting numbers lower than
[01:21:21] one.
[01:21:23] And if you plug in numbers greater than
[01:21:25] zero, you're getting numbers greater
[01:21:27] than one
[01:21:28] all the way growing to the infinity.
[01:21:30] And this here grows to zero.
[01:21:33] So, basically we're going to take these
[01:21:36] numbers
[01:21:37] here.
[01:21:40] And
[01:21:43] instead of them being positive and
[01:21:44] negative in all of the place, we're
[01:21:46] going to interpret them as log counts
[01:21:48] and then we're going to element-wise
[01:21:50] exponentiate these numbers.
[01:21:52] Exponentiating them now gives us
[01:21:54] something like this.
[01:21:56] And you see that these numbers now
[01:21:57] because of they went through an
[01:21:58] exponent, all the negative numbers
[01:22:00] turned into numbers below one like
[01:22:02] 0.338.
[01:22:04] And all the positive numbers originally
[01:22:06] turned into even more positive numbers
[01:22:08] sort of greater than one.
[01:22:10] Um so, like for example, seven
[01:22:13] um is some positive number over here. Um
[01:22:18] that is greater than zero.
[01:22:21] But, exponentiated outputs here
[01:22:24] um basically give us something that we
[01:22:26] can use and interpret as the equivalent
[01:22:28] of counts or originally. So, you see
[01:22:31] these counts here, 1 12 7 51 1 etc.
[01:22:36] The neural net is kind of now predicting
[01:22:39] uh
[01:22:40] counts.
[01:22:41] And these counts are positive numbers.
[01:22:44] They can never be below zero, so that
[01:22:45] makes sense. And uh they can now take on
[01:22:48] various values
[01:22:49] depending on the settings of W.
[01:22:54] So, let me break this down.
[01:22:56] We're going to interpret these to be the
[01:22:58] log counts.
[01:23:01] Another word for this that is often used
[01:23:03] is so-called logits.
[01:23:05] These are logits, log counts.
[01:23:08] And these will be sort of the counts.
[01:23:11] Logits exponentiated.
[01:23:13] And this is equivalent to the N matrix,
[01:23:16] sort of, the N
[01:23:18] array that we used previously. Remember,
[01:23:20] this was the N.
[01:23:21] This is the the array of counts. And
[01:23:24] each row here are the counts for the
[01:23:27] for the um
[01:23:28] next character, sort of.
[01:23:32] So, those are the counts. And now the
[01:23:34] probabilities are just the counts um
[01:23:38] normalized.
[01:23:39] And so, um
[01:23:41] I'm not going to find the same, but
[01:23:43] basically, I'm not going to scroll all
[01:23:44] over the place.
[01:23:46] We've already done this. We want to
[01:23:48] counts that sum along the first
[01:23:50] dimension, and we want to keep dims as
[01:23:53] true.
[01:23:54] We went over this, and this is how we
[01:23:56] normalize the rows of our counts matrix
[01:24:00] to get our probabilities.
[01:24:03] probs
[01:24:04] So, now these are the probabilities.
[01:24:07] And these are the counts that we have
[01:24:10] currently. And now when I show the
[01:24:11] probabilities,
[01:24:13] you see that um
[01:24:15] every row here,
[01:24:17] of course,
[01:24:19] will sum to one
[01:24:21] because they're normalized.
[01:24:23] And the shape of this
[01:24:25] is 5 by 27.
[01:24:27] And so really what we've achieved is for
[01:24:29] every one of our five examples, we now
[01:24:32] have a row that came out of a neural
[01:24:34] net.
[01:24:35] And because of the transformations here,
[01:24:37] we made sure that this output of this
[01:24:39] neural net now are probabilities or we
[01:24:41] can interpret to be probabilities.
[01:24:44] So,
[01:24:45] our WX here gave us logits
[01:24:48] and then we interpret those to be log
[01:24:49] counts.
[01:24:50] We exponentiate to get something that
[01:24:52] looks like counts.
[01:24:54] And then we normalize those counts to
[01:24:55] get a probability distribution.
[01:24:57] And all of these are differentiable
[01:24:59] operations.
[01:25:00] So, what we've done now is we are taking
[01:25:02] inputs.
[01:25:03] We have differentiable operations that
[01:25:04] we can back propagate through
[01:25:07] and we're getting out probability
[01:25:08] distributions.
[01:25:09] So, um for example, for the zeroth
[01:25:12] example that fed in,
[01:25:15] right, which was um
[01:25:17] the zeroth example here was a one-hot
[01:25:18] vector of zero.
[01:25:20] And um
[01:25:22] it basically corresponded to feeding in
[01:25:26] uh
[01:25:26] this example here. So, we're feeding in
[01:25:28] a dot into a neural net. And the way we
[01:25:30] fed the dot into a neural net is that we
[01:25:32] first got its index.
[01:25:34] Then we one-hot encoded it.
[01:25:36] Then it went into the neural net and out
[01:25:39] came
[01:25:40] this distribution of probabilities.
[01:25:43] And its shape
[01:25:46] is 27. There's 27 numbers and we're
[01:25:49] going to interpret this as the neural
[01:25:51] net's assignment for how likely
[01:25:54] every one of these characters um
[01:25:56] the 27 characters are to come next.
[01:25:59] And as we tune the weights W,
[01:26:02] we're going to be of course getting
[01:26:03] different probabilities out for any
[01:26:05] character that you input.
[01:26:07] And so now the question is just can we
[01:26:08] optimize and find a good W
[01:26:11] such that the probabilities coming out
[01:26:13] are pretty good. And the way we measure
[01:26:15] pretty good is by the loss function.
[01:26:17] Okay, so I organized everything into a
[01:26:18] single summary so that hopefully it's a
[01:26:20] bit more clear. So it starts here.
[01:26:22] We have an input data set.
[01:26:24] We have some inputs to the neural net
[01:26:26] and we have some labels for the correct
[01:26:28] next character in a sequence. And these
[01:26:30] are integers.
[01:26:32] Here I'm using uh torch generators now
[01:26:35] so that you see the same numbers that I
[01:26:37] see.
[01:26:38] And I'm generating
[01:26:40] um
[01:26:40] 27 neurons weights
[01:26:42] and each neuron here receives 27 inputs.
[01:26:48] Then here we're going to plug in all the
[01:26:50] input examples x's into a neural net. So
[01:26:52] here, this is a forward pass.
[01:26:55] First, we have to encode all of the
[01:26:57] inputs into one-hot representations.
[01:27:00] So we have 27 classes, we pass in these
[01:27:02] integers and x inc becomes a array that
[01:27:07] is 5 by 27.
[01:27:09] Zeros except for a few ones.
[01:27:12] We then multiply this in the first layer
[01:27:14] of a neural net to get logits.
[01:27:16] Exponentiate the logits to get fake
[01:27:18] counts, sort of.
[01:27:20] And normalize these counts to get
[01:27:22] probabilities.
[01:27:24] So the la- these last two lines by the
[01:27:26] way here are called the softmax.
[01:27:29] Uh which I pulled up here.
[01:27:32] Softmax is a very often used layer in a
[01:27:34] neural net that takes these z's which
[01:27:37] are logits,
[01:27:38] exponentiates them,
[01:27:40] and uh divides and normalizes. It's a
[01:27:43] way of taking outputs of a neural net
[01:27:45] layer and these uh these outputs can be
[01:27:47] positive or negative.
[01:27:49] And it outputs probability
[01:27:51] distributions. It outputs something that
[01:27:53] is always sums to one and are positive
[01:27:56] numbers, just like probabilities.
[01:27:58] Um so it's kind of like a normalization
[01:28:00] function if you want to think of it that
[01:28:01] way. And you can put it on top of any
[01:28:03] other linear layer inside a neural net
[01:28:05] and it basically makes a neural net
[01:28:07] output probabilities. That's very often
[01:28:09] used and we used it as well here.
[01:28:13] So this is the forward pass and that's
[01:28:14] how we made a neural net output
[01:28:16] probability.
[01:28:17] Now
[01:28:19] you'll notice that
[01:28:20] um
[01:28:23] all of these
[01:28:24] this entire forward pass is made up of
[01:28:26] differentiable
[01:28:27] layers. Everything here we can back
[01:28:29] propagate through. And we saw some of
[01:28:30] the back propagation in micrograd.
[01:28:33] This is just
[01:28:34] multiplication and addition. All that's
[01:28:36] happening here is just multiply and then
[01:28:38] add. And we know how to back propagate
[01:28:39] through them.
[01:28:40] Exponentiation we know how to back
[01:28:42] propagate through.
[01:28:43] And then here we are summing and sum is
[01:28:47] is easily back propagatable as well.
[01:28:50] And division as well. So everything here
[01:28:52] is differentiable operation
[01:28:54] and we can back propagate through.
[01:28:57] Now we achieve these probabilities which
[01:28:59] are 5 by 27.
[01:29:01] For every single example we have a
[01:29:03] vector of probabilities that sum to one.
[01:29:06] And then here I wrote a bunch of stuff
[01:29:08] uh to sort of like break down uh the
[01:29:10] examples.
[01:29:11] So we have five examples making up Emma,
[01:29:14] right?
[01:29:16] And there are five bigrams inside Emma.
[01:29:20] So bigram example a bigram example one
[01:29:23] is that E is the beginning character
[01:29:26] right after dot.
[01:29:28] And the indexes for these are zero and
[01:29:30] five.
[01:29:31] So then we feed in a zero.
[01:29:34] That's the input to the neural net.
[01:29:36] We get probabilities from the neural net
[01:29:38] that are 27 numbers.
[01:29:41] And then the label is five because E
[01:29:44] actually comes after dot.
[01:29:45] So that's the label.
[01:29:47] And then
[01:29:49] we use this label five to index into the
[01:29:52] probability distribution here.
[01:29:54] So this index five here is 0 1 2 3 4 5.
[01:29:59] It's this number here.
[01:30:01] Which is here.
[01:30:04] So that's basically the probability
[01:30:05] assigned by the neural net to the actual
[01:30:07] correct character.
[01:30:08] You see that the network currently
[01:30:10] thinks that this next character that E
[01:30:12] following dot is only 1% likely. Which
[01:30:15] is of course not very good, right?
[01:30:17] Because this actually is a training
[01:30:18] example and the network thinks that this
[01:30:20] is currently very very unlikely. But
[01:30:22] that's just because we didn't get very
[01:30:24] lucky in generating a good setting of W.
[01:30:27] So right now this network thinks this is
[01:30:28] unlikely and 0.01 is not a good outcome.
[01:30:32] So the log likelihood then
[01:30:34] is very negative.
[01:30:36] And the negative log likelihood is very
[01:30:38] positive.
[01:30:39] And so four is a very high negative log
[01:30:42] likelihood and that means we're going to
[01:30:44] have a high loss.
[01:30:45] Because what is the loss? The loss is
[01:30:47] just the average negative log
[01:30:49] likelihood.
[01:30:51] So the second character is E M.
[01:30:53] And you see here that also the network
[01:30:55] thought that M following E is very
[01:30:57] unlikely, 1%.
[01:31:00] Uh the for M following M it thought it
[01:31:02] was 2%.
[01:31:04] And for A following M it actually
[01:31:06] thought it was 7% likely. So just by
[01:31:09] chance this one actually has a pretty
[01:31:11] good probability and therefore a pretty
[01:31:12] low negative log likelihood.
[01:31:15] And finally here it thought this was 1%
[01:31:17] likely.
[01:31:18] So overall our average negative log
[01:31:20] likelihood, which is the loss, the total
[01:31:22] loss that summarizes basically the how
[01:31:25] well this network currently works at
[01:31:27] least on this one word, not on the full
[01:31:29] data set, just the one word, is 3.76.
[01:31:32] Which is actually very fairly high loss.
[01:31:34] This is not a very good setting of Ws.
[01:31:36] Now here's what we can do.
[01:31:38] We're currently getting 3.76.
[01:31:41] We can actually come here and we can
[01:31:42] change our W. We can resample it. So let
[01:31:45] me just add one to have a different
[01:31:47] seed.
[01:31:48] And then we get a different W.
[01:31:50] And then we can rerun this.
[01:31:52] And with this different seed with this
[01:31:54] different setting of Ws we now get 3.37.
[01:31:58] So this is a much better W, right? And
[01:32:00] that and it's better because the
[01:32:02] probability just happened to come out
[01:32:04] higher for the for the characters that
[01:32:07] actually are next.
[01:32:08] And so you can imagine actually just
[01:32:10] resampling this, you know, we can try
[01:32:12] two.
[01:32:14] So
[01:32:15] Okay, this was not very good.
[01:32:17] Let's try one more.
[01:32:18] We can try three.
[01:32:20] Okay, this was terrible setting because
[01:32:22] we have a very high loss.
[01:32:24] So
[01:32:26] anyway, I'm going to erase this.
[01:32:29] What what I'm doing here, which is just
[01:32:31] guess and check of randomly assigning
[01:32:33] parameters and seeing if the network is
[01:32:34] good, that is amateur hour. That's not
[01:32:37] how you optimize a neural net. The way
[01:32:39] you optimize a neural net is you start
[01:32:41] with some random guess, and we're going
[01:32:42] to commit to this one even though it's
[01:32:43] not very good.
[01:32:45] But now the big deal is we have a loss
[01:32:46] function.
[01:32:48] So this loss
[01:32:50] is made up only of differentiable
[01:32:52] operations.
[01:32:54] And we can minimize the loss by tuning
[01:32:57] W's by computing the gradients of the
[01:33:00] loss with respect to these W matrices.
[01:33:05] And so then we can tune W to minimize
[01:33:07] the loss and find a good setting of W
[01:33:09] using gradient-based optimization. So
[01:33:11] let's see how that will work. Now things
[01:33:13] are actually going to look almost
[01:33:14] identical to what we had with micrograd.
[01:33:17] So here I pulled up the lecture from
[01:33:20] micrograd, the notebook. It's from this
[01:33:22] repository.
[01:33:23] And when I scroll all the way to the end
[01:33:25] where we left off with micrograd, we had
[01:33:26] something very very similar.
[01:33:28] We had a number of input examples. In
[01:33:31] this case, we had four input examples
[01:33:32] inside X's.
[01:33:34] And we had their targets. These are
[01:33:36] targets.
[01:33:37] Just like here, we have our X's now, but
[01:33:39] we have five of them, and they're now
[01:33:41] integers instead of vectors.
[01:33:44] But we're going to convert our integers
[01:33:46] to vectors, except our vectors will be
[01:33:47] 27 large instead of three large.
[01:33:51] And then here what we did is first we
[01:33:53] did a forward pass where where ran a
[01:33:55] neural net on all of the inputs
[01:33:58] to get predictions.
[01:34:00] Our neural net at the time, this NFX,
[01:34:02] was a net a multi-layer perceptron.
[01:34:05] Our neural net is going to look
[01:34:06] different because our neural net is just
[01:34:08] a single layer.
[01:34:10] Single linear layer followed by a
[01:34:12] softmax.
[01:34:13] So, that's our neural net.
[01:34:15] And the loss here was the mean squared
[01:34:17] error. So, we simply subtracted the
[01:34:19] prediction from the ground truth and
[01:34:21] squared it and summed it all up. And
[01:34:23] that was the loss. And loss was the
[01:34:24] single number that summarized the
[01:34:26] quality of the neural net. And when loss
[01:34:29] is low, like almost zero, that means the
[01:34:32] neural net is um
[01:34:33] predicting correctly.
[01:34:36] So, we had a single number that uh that
[01:34:38] summarized the
[01:34:40] uh the performance of the neural net.
[01:34:42] And everything here was differentiable
[01:34:43] and was stored in massive compute graph.
[01:34:46] And then we iterated over all the
[01:34:48] parameters. We made sure that the
[01:34:50] gradients are set to zero.
[01:34:51] And we called loss.backward.
[01:34:54] And loss.backward initiated
[01:34:55] backpropagation at the final output node
[01:34:58] of loss. Right? So,
[01:35:00] yeah, remember these expressions? We had
[01:35:02] loss all the way at the end. We start
[01:35:03] backpropagation and we went all the way
[01:35:05] back.
[01:35:06] And we made sure that we populated all
[01:35:08] the parameters.grad.
[01:35:10] So, that grad started at zero, but
[01:35:12] backpropagation filled it in.
[01:35:14] And then in the update, we iterated over
[01:35:16] all the parameters and we simply did a
[01:35:18] parameter update where every single uh
[01:35:21] element of our parameters was nudged in
[01:35:24] the opposite direction of the gradient.
[01:35:27] And so, we're going to do the exact same
[01:35:30] thing here.
[01:35:31] Uh so, I'm going to pull this up
[01:35:34] on the side here
[01:35:38] so that we have it available. And we're
[01:35:40] actually going to do the exact same
[01:35:41] thing.
[01:35:42] So, this was the forward pass. So, where
[01:35:44] we did this.
[01:35:46] And probs is our Ypred.
[01:35:49] So, now we have to evaluate the loss,
[01:35:50] but we're not using the mean squared
[01:35:51] error. we're using the negative log
[01:35:53] likelihood because we are doing
[01:35:54] classification, we're not doing
[01:35:56] regression, as it's called.
[01:35:59] So, here we want to calculate loss.
[01:36:02] Now, the way we calculate it is is just
[01:36:04] this average negative log likelihood.
[01:36:07] Now, this probs here
[01:36:10] has a shape of 5 by 27.
[01:36:13] And so, to get all the we basically want
[01:36:15] to pluck out the probabilities at the
[01:36:18] correct indices here.
[01:36:20] So, in particular, because the labels
[01:36:21] are stored here in the array wise,
[01:36:24] basically what we're after is for the
[01:36:26] first example, we're looking at
[01:36:27] probability of five, right? At index
[01:36:30] five.
[01:36:31] For the second example,
[01:36:32] at the the second row or row index one,
[01:36:36] we are interested in the probability
[01:36:37] assigned to index 13.
[01:36:40] At the second example, we also have 13.
[01:36:43] At the third row, we want one.
[01:36:47] And at the last row, which is four, we
[01:36:49] want zero. So, these are the
[01:36:51] probabilities we're interested in,
[01:36:53] right?
[01:36:54] And you can see that they're not amazing
[01:36:56] as we saw above.
[01:36:58] So, these are the probabilities we want,
[01:37:00] but we want like a more efficient way to
[01:37:02] access these probabilities. Uh not just
[01:37:05] listing them out in a tuple like this.
[01:37:07] So, it turns out that the way to do this
[01:37:08] in PyTorch, uh one of the ways at least,
[01:37:10] is we can basically pass in all of these
[01:37:16] Sorry about that. All of these um
[01:37:19] integers in a vectors.
[01:37:22] So, the
[01:37:23] these ones, you see how they're just 0 1
[01:37:25] 2 3 4,
[01:37:27] we can actually create that using MP not
[01:37:29] MP, sorry, torch.arange of five.
[01:37:32] 0 1 2 3 4.
[01:37:34] So, we can index here with torch.arange
[01:37:36] of five.
[01:37:38] And here, we index with wise.
[01:37:41] And you see that that gives us
[01:37:43] exactly these numbers.
[01:37:49] So, that plugs out the probabilities of
[01:37:51] that the neural network assigns to the
[01:37:54] correct next character.
[01:37:56] Now, we take those probabilities and we
[01:37:58] don't we actually look at the log
[01:37:59] probability. So, we want to dot log.
[01:38:03] And then, we want to just average that
[01:38:06] up. So, take the mean of all of that.
[01:38:08] And then, it's the negative average log
[01:38:11] likelihood that is the loss.
[01:38:14] So, the loss here is
[01:38:16] 3.7 something. And you see that this
[01:38:18] loss, 3.76, 3.76 is exactly as we've
[01:38:22] obtained before, but this is a
[01:38:23] vectorized form of that expression.
[01:38:26] So, we get the same loss.
[01:38:29] And this same loss we can consider sort
[01:38:31] of as part of this forward pass.
[01:38:34] And we've achieved here now loss.
[01:38:36] Okay, so we made our way all the way to
[01:38:37] loss. We defined the forward pass. We
[01:38:40] forwarded the network and the loss. Now,
[01:38:42] we're ready to do backward pass.
[01:38:44] So, backward pass.
[01:38:48] We want to first make sure that all the
[01:38:49] gradients are reset. So, they're at
[01:38:51] zero.
[01:38:52] Now, in PyTorch, you can set the
[01:38:55] gradients to be zero, but you can also
[01:38:56] just set it to none. And setting it to
[01:38:58] none is more efficient. And PyTorch will
[01:39:00] interpret none as like a lack of a
[01:39:03] gradient and is the same as zeros.
[01:39:05] So, this is a way to set to zero the
[01:39:07] gradient.
[01:39:10] And now, we do loss.backward.
[01:39:14] Before we do loss.backward, we need one
[01:39:16] more thing. If you remember from
[01:39:17] micrograd,
[01:39:19] PyTorch actually requires
[01:39:21] that we pass in requires_grad is true.
[01:39:25] Uh so that we tell
[01:39:27] PyTorch that we are interested in
[01:39:28] calculating gradients for this leaf
[01:39:30] tensor. By default, this is false.
[01:39:33] So, let me recalculate with that.
[01:39:36] And then, set to none and loss.backward.
[01:39:40] Now, something magical happened when
[01:39:42] loss of backward was run.
[01:39:44] Because PyTorch, just like micrograd,
[01:39:47] when we did the forward pass here,
[01:39:49] it keeps track of all the operations
[01:39:51] under the hood. It builds a full
[01:39:53] computational graph.
[01:39:54] Just like the graphs we could produce in
[01:39:57] micrograd, those graphs exist inside
[01:39:59] PyTorch.
[01:40:00] And so, it knows all the dependencies
[01:40:02] and all the mathematical operations of
[01:40:04] everything.
[01:40:05] And when you then calculate the loss, we
[01:40:07] can call a dot backward on it.
[01:40:09] And dot backward then fills in the
[01:40:11] gradients of all the intermediates all
[01:40:15] the way back to W's, which are the
[01:40:18] parameters of our neural net. So, now we
[01:40:20] can do W.grad,
[01:40:22] and we see that it has structure.
[01:40:23] There's stuff inside it.
[01:40:29] And these gradients, every single
[01:40:31] element here,
[01:40:33] so W.shape is 27 by 27.
[01:40:36] W.grad's shape is the same, 27 by 27.
[01:40:40] And every element of W.grad
[01:40:43] is telling us
[01:40:44] the influence of that weight on the loss
[01:40:47] function.
[01:40:48] So, for example, this number all the way
[01:40:50] here,
[01:40:52] if this element, the 0 0 element of W,
[01:40:55] because the gradient is positive, it's
[01:40:57] telling us that this has a positive
[01:41:00] influence on the loss, slightly nudging
[01:41:03] W
[01:41:04] slightly taking W00
[01:41:06] and adding a small H to it
[01:41:10] would increase the loss mildly because
[01:41:13] this gradient is positive.
[01:41:15] Some of these gradients are also
[01:41:16] negative.
[01:41:18] So, that's telling us about the gradient
[01:41:20] information, and we can use this
[01:41:22] gradient information to update the
[01:41:24] weights of this neural network. So,
[01:41:26] let's now do the update. It's going to
[01:41:28] be very similar to what we had in
[01:41:29] micrograd. We need no uh loop over all
[01:41:32] the parameters because we only have one
[01:41:34] parameter uh tensor, and that is W. So,
[01:41:37] we simply do W.data plus equals uh, the
[01:41:42] We can actually copy this almost
[01:41:43] exactly. -0.1 *
[01:41:46] uh, W.grad.
[01:41:48] Um,
[01:41:49] and that would be the update to the
[01:41:52] tensor.
[01:41:54] So, that updates the tensor.
[01:41:58] And because the tensor is updated, we
[01:42:01] would expect that now the loss should
[01:42:03] decrease.
[01:42:04] So, here, if I print loss
[01:42:09] .item,
[01:42:11] it was 3.76, right? So, we've updated
[01:42:14] the W here. So, if I recalculate forward
[01:42:17] pass,
[01:42:18] loss now should be slightly lower. So,
[01:42:21] 3.76 goes to
[01:42:23] 3.74.
[01:42:25] And then, we can again set to set grad
[01:42:28] to none and backward update.
[01:42:32] And now the parameters changed again.
[01:42:34] So, if we recalculate the forward pass,
[01:42:37] we expect a lower loss again, 3.72.
[01:42:42] Okay, and this is again doing the We're
[01:42:44] now doing gradient descent.
[01:42:48] And when we achieve a low loss, that
[01:42:50] will mean that the network is assigning
[01:42:52] high probabilities to the correct next
[01:42:54] characters. Okay, so I rearranged
[01:42:56] everything and I put it all together
[01:42:58] from scratch.
[01:42:59] So, here is where we construct our data
[01:43:01] set of bigrams.
[01:43:03] You see that we are still iterating only
[01:43:04] on the first word, Emma.
[01:43:06] I'm going to change that in a second. I
[01:43:09] added a number that counts the number of
[01:43:11] elements in X's, so that we explicitly
[01:43:14] see the number of examples is five.
[01:43:16] Because currently we're just working
[01:43:18] with Emma, and there's five bigrams
[01:43:19] there.
[01:43:20] And here I added a loop of exactly what
[01:43:22] we had before. So, we had 10 iterations
[01:43:25] of gradient descent, of forward pass,
[01:43:27] backward pass, and an update. And so,
[01:43:29] running these two cells, initialization
[01:43:31] and gradient descent
[01:43:32] gives us some improvement on uh the loss
[01:43:36] function.
[01:43:38] But now, I want to use all the words.
[01:43:41] And there's not five, but 228,000
[01:43:44] bigrams now.
[01:43:46] However, this should require no
[01:43:48] modification whatsoever. Everything
[01:43:49] should just run because all the code we
[01:43:51] wrote doesn't care if there's five
[01:43:53] bigrams or 228,000 bigrams. And with
[01:43:56] everything, we should just work. So,
[01:43:58] you see that this will just run.
[01:44:00] But now we are optimizing over the
[01:44:01] entire training set of all the bigrams.
[01:44:04] And you see now that we are decreasing
[01:44:06] very slightly. So, actually, we can
[01:44:08] probably afford a larger learning rate.
[01:44:12] We can probably afford even larger
[01:44:13] learning rate.
[01:44:20] Even 50 seems to work on this very, very
[01:44:22] simple example, right? So, let me
[01:44:24] re-initialize, and let's run 100
[01:44:26] iterations.
[01:44:29] See what happens.
[01:44:33] Okay.
[01:44:36] We seem to be
[01:44:39] coming up to some pretty good losses
[01:44:40] here. 2.47.
[01:44:42] Let me run 100 more.
[01:44:44] What is the number that we expect, by
[01:44:46] the way, in the loss? We expect to get
[01:44:48] something around what we had originally,
[01:44:50] actually.
[01:44:52] So, all the way back, if you remember,
[01:44:53] in the beginning of this video, when we
[01:44:55] optimized uh just by counting,
[01:44:58] our loss was roughly 2.47
[01:45:01] after we added smoothing.
[01:45:03] But before smoothing, we had roughly
[01:45:04] 2.45
[01:45:06] uh likelihood.
[01:45:08] Um sorry, loss.
[01:45:09] And so, that's actually roughly the
[01:45:11] vicinity of what we expect to achieve.
[01:45:13] But before we achieved it by counting,
[01:45:15] and here we are achieving the roughly
[01:45:17] the same result, but with gradient-based
[01:45:19] optimization.
[01:45:21] So, we come to about 2.4
[01:45:23] 6, 2.45, etc.
[01:45:26] And that makes sense because
[01:45:27] fundamentally, we're not taking any
[01:45:28] additional information. We're still just
[01:45:30] taking in the previous character and
[01:45:31] trying to predict the next one. But
[01:45:33] instead of doing it explicitly by
[01:45:35] counting and normalizing,
[01:45:38] we are doing it with gradient-based
[01:45:39] learning. And it just so happens that
[01:45:41] the explicit approach happens to very
[01:45:43] well optimize the loss function without
[01:45:46] any need for gradient-based optimization
[01:45:48] because the setup for bigram language
[01:45:50] models are is is so straightforward and
[01:45:52] so simple. We can just afford to
[01:45:54] estimate those probabilities directly
[01:45:55] and maintain them in a table.
[01:45:58] But the gradient-based approach is
[01:46:00] significantly more flexible.
[01:46:03] So we've actually gained a lot because
[01:46:06] what we can do now is um
[01:46:09] we can expand this approach and
[01:46:11] complexify the neural net.
[01:46:12] So currently we're just taking a single
[01:46:14] character and feeding into a neural net
[01:46:15] and the neural net is extremely simple.
[01:46:17] But we're about to iterate on this
[01:46:19] substantially. We're going to be taking
[01:46:21] multiple previous characters and we're
[01:46:23] going to be feed them in feeding them
[01:46:25] into increasingly more complex neural
[01:46:26] nets. But fundamentally uh the output of
[01:46:29] the neural net will always just be
[01:46:30] logits.
[01:46:32] And those logits will go through the
[01:46:34] exact same transformation. We are going
[01:46:36] to take them through a softmax,
[01:46:38] calculate the loss function and the
[01:46:39] negative log likelihood,
[01:46:41] and do gradient-based optimization.
[01:46:43] And so actually as we complexify the
[01:46:46] neural nets and work all the way up to
[01:46:48] transformers,
[01:46:49] none of this will really fundamentally
[01:46:51] change. None of this will fundamentally
[01:46:52] change. The only thing that will change
[01:46:54] is
[01:46:55] the way we do the forward pass where we
[01:46:57] take in some previous characters and
[01:46:59] calculate the logits for the next
[01:47:01] character in a sequence. That will
[01:47:03] become more complex
[01:47:05] and uh but we'll use the same machinery
[01:47:07] to optimize it.
[01:47:08] And um
[01:47:10] it's not obvious how we would have
[01:47:12] extended this bigram approach into the
[01:47:15] case where there are many more
[01:47:17] characters at the input because
[01:47:19] eventually these tables would get way
[01:47:21] too large because there's way too many
[01:47:23] combinations of what previous characters
[01:47:26] uh could be.
[01:47:27] If you only have one previous character,
[01:47:29] we can just keep everything in a table,
[01:47:31] the counts. But if you have the last 10
[01:47:33] characters that are input, we can't
[01:47:35] actually keep everything in a table
[01:47:36] anymore. So this is fundamentally an
[01:47:38] unscalable approach, and the neural
[01:47:40] network approach is significantly more
[01:47:42] scalable, and it's something that
[01:47:44] actually we can improve on over time. So
[01:47:46] that's where we will be digging next. I
[01:47:48] wanted to point out two more things.
[01:47:51] Number one,
[01:47:52] I want you to notice that this
[01:47:55] X inc here,
[01:47:56] this is made up of one-hot vectors, and
[01:47:59] then those one-hot vectors are
[01:48:00] multiplied by this W matrix.
[01:48:03] And we think of this as uh multiple
[01:48:05] neurons being forwarded in a fully
[01:48:07] connected manner.
[01:48:08] But actually what's happening here is
[01:48:10] that, for example,
[01:48:12] if you have a one-hot vector here that
[01:48:14] has a one at, say, the fifth dimension,
[01:48:17] then because of the way the matrix
[01:48:19] multiplication works,
[01:48:21] multiplying that one-hot vector with W
[01:48:23] actually ends up plucking out the fifth
[01:48:25] row of W.
[01:48:27] Logits would become just a fifth row of
[01:48:30] W.
[01:48:31] And that's because of the way the matrix
[01:48:33] multiplication works.
[01:48:35] Um
[01:48:36] so that's actually what ends up
[01:48:38] happening.
[01:48:40] So but that's actually exactly what
[01:48:42] happened before.
[01:48:43] Because remember all the way up here,
[01:48:46] we have a bigram. We took the first
[01:48:48] character, and then that first character
[01:48:50] indexed into a row of this array here.
[01:48:55] And that row gave us the probability
[01:48:56] distribution for the next character.
[01:48:58] So the first character was used as a
[01:49:00] lookup into a
[01:49:02] uh
[01:49:03] matrix here to get the probability
[01:49:05] distribution.
[01:49:06] Well, that's actually exactly what's
[01:49:07] happening here.
[01:49:08] Because we're taking the index, we're
[01:49:10] encoding it as one-hot, and multiplying
[01:49:12] it by W.
[01:49:13] So logits literally becomes the
[01:49:16] uh the
[01:49:18] the appropriate row of W.
[01:49:20] And that gets just as before
[01:49:22] exponentiated to create the counts
[01:49:25] and then normalized and becomes
[01:49:26] probability.
[01:49:27] So this W here
[01:49:29] is literally
[01:49:31] the same as this array here.
[01:49:35] But W, remember, is the log counts, not
[01:49:38] the counts. So it's more precise to say
[01:49:40] that W exponentiated
[01:49:42] W.exp is this array.
[01:49:46] But this array was filled in by counting
[01:49:49] and by basically
[01:49:52] populating the counts of bigrams,
[01:49:53] whereas in the gradient-based framework,
[01:49:55] we initialize it randomly and then we
[01:49:57] let the loss guide us
[01:50:00] to arrive at the exact same array.
[01:50:03] So this array exactly here
[01:50:05] is
[01:50:06] basically the array W at the end of
[01:50:09] optimization, except we arrived at it
[01:50:12] piece by piece by following the loss.
[01:50:15] And that's why we also obtain the same
[01:50:16] loss function at the end. And the second
[01:50:18] note is if I come here,
[01:50:20] remember the smoothing where we added
[01:50:22] fake counts to our counts in order to
[01:50:26] smooth out and make more uniform the
[01:50:28] distributions of these probabilities.
[01:50:31] And that prevented us from assigning
[01:50:32] zero probability to
[01:50:34] um
[01:50:35] to any one bigram.
[01:50:37] Now, if I increase the count here,
[01:50:40] what's happening to the probability?
[01:50:42] As I increase the count, probability
[01:50:45] becomes more and more uniform.
[01:50:48] Right? Because these counts go only up
[01:50:50] to like 900 or whatever. So if I'm
[01:50:51] adding plus a million to every single
[01:50:54] number here, you can see how uh the row
[01:50:57] and its probability then when we divide
[01:50:59] is just going to become more and more
[01:51:00] close to exactly even probability,
[01:51:03] uniform distribution.
[01:51:05] It turns out that the gradient-based
[01:51:06] framework has an equivalent to
[01:51:09] smoothing.
[01:51:10] In particular,
[01:51:13] think through these W's here,
[01:51:15] which we initialized randomly.
[01:51:18] We could also think about initializing
[01:51:20] W's to be zero.
[01:51:22] If all the entries of W are zero,
[01:51:26] then you'll see that logits will become
[01:51:27] all zero.
[01:51:28] And then exponentiating those logits
[01:51:30] becomes all one.
[01:51:32] And then the probabilities turn out to
[01:51:33] be exactly uniform.
[01:51:35] So, basically when W's are all equal to
[01:51:38] each other, or say especially zero,
[01:51:41] then the probabilities come out
[01:51:42] completely uniform.
[01:51:44] So,
[01:51:45] trying to incentivize W to be near zero
[01:51:49] is basically equivalent to label
[01:51:52] smoothing. And the more you incentivize
[01:51:54] that in the loss function, the more
[01:51:56] smooth distribution you're going to
[01:51:57] achieve.
[01:51:58] So, this brings us to something that's
[01:52:00] called regularization,
[01:52:02] where we can actually augment the loss
[01:52:03] function to have a small component that
[01:52:06] we call a regularization loss.
[01:52:09] In particular, what we're going to do is
[01:52:10] we can take W,
[01:52:11] and we can for example square all of its
[01:52:13] entries,
[01:52:14] and then we can uh oops.
[01:52:17] Sorry about that.
[01:52:19] We can take all the entries of W, and we
[01:52:20] can sum them.
[01:52:23] And because we're squaring, uh there
[01:52:25] will be no signs anymore. Um
[01:52:28] negatives and positives all get squashed
[01:52:30] to be positive numbers.
[01:52:31] And then the way this works is you
[01:52:33] achieve zero loss if W is exactly or
[01:52:36] zero.
[01:52:37] But if W has non-zero numbers, you
[01:52:39] accumulate loss.
[01:52:41] And so, we can actually take this, and
[01:52:42] we can add it on here.
[01:52:44] So, we can do something like loss plus
[01:52:48] W squared
[01:52:50] dot sum.
[01:52:52] Or let's actually, instead of sum, let's
[01:52:53] take a mean, cuz otherwise the sum gets
[01:52:55] too large.
[01:52:57] So, mean is like a little bit more
[01:52:58] manageable.
[01:53:01] And then we have a regularization loss
[01:53:02] here, let's say 0.01 times,
[01:53:05] or something like that. You can choose
[01:53:06] the regularization strength.
[01:53:09] And then we can just optimize this.
[01:53:12] And now this optimization actually has
[01:53:14] two components. Not only is it trying to
[01:53:16] make all the probabilities work out, but
[01:53:18] in addition to that, there's an
[01:53:19] additional component that simultaneously
[01:53:21] tries to make all W's be zero. Because
[01:53:24] if W's are non-zero, you feel a loss.
[01:53:26] And so minimizing this, the only way to
[01:53:28] do achieve that is for W to be zero.
[01:53:30] And so you can think of this as adding
[01:53:32] like a spring force or like a gravity
[01:53:34] force that that pushes W to be zero.
[01:53:37] So W wants to be zero, and the
[01:53:39] probabilities want to be uniform, but
[01:53:41] they also simultaneously want to match
[01:53:43] up your your probabilities as indicated
[01:53:46] by the data.
[01:53:47] And so the strength of this
[01:53:49] regularization is exactly controlling
[01:53:52] the amount of counts
[01:53:54] that you add here.
[01:53:57] Adding a lot more counts here
[01:54:00] corresponds to
[01:54:02] increasing this number.
[01:54:04] Because the more you increase it, the
[01:54:06] more this part of the loss function
[01:54:08] dominates this part, and the more these
[01:54:10] these weights will be unable to grow
[01:54:13] because as they grow,
[01:54:15] they accumulate way too much loss.
[01:54:18] And so if this is strong enough,
[01:54:21] then we are not able to overcome the
[01:54:23] force of this loss, and we will never
[01:54:26] and basically everything will be uniform
[01:54:28] predictions.
[01:54:29] So I thought that's kind of cool.
[01:54:30] Okay, and lastly, before we wrap up,
[01:54:33] I wanted to show you how you would
[01:54:34] sample from this neural net model.
[01:54:36] And I copy-pasted the sampling code from
[01:54:39] before.
[01:54:40] Where remember that we sampled five
[01:54:43] times.
[01:54:44] And all we did is we started zero, we
[01:54:46] grabbed the current IX row of P.
[01:54:50] And that was our probability row
[01:54:52] from which we sampled the next index and
[01:54:55] just accumulated that and break when
[01:54:57] zero.
[01:54:58] And running this gave us these results.
[01:55:03] I still have the
[01:55:05] P in memory, so this is fine.
[01:55:07] Now,
[01:55:09] this P doesn't come from the row of P.
[01:55:12] Instead, it comes from this neural net.
[01:55:14] First, we take IX
[01:55:17] and we encode it into a one-hot row of X
[01:55:21] inc.
[01:55:22] This X inc multiplies our W,
[01:55:25] which really just plucks out the row of
[01:55:26] W corresponding to IX. Really, that's
[01:55:29] what's happening.
[01:55:30] And that gets our logits, and then we
[01:55:33] normalize those logits, exponentiate to
[01:55:35] get counts, and then normalize to get uh
[01:55:37] the distribution, and then we can sample
[01:55:39] from the distribution.
[01:55:41] So, if I run this,
[01:55:45] kind of anticlimactic or climatic,
[01:55:47] depending how you look at it, but we get
[01:55:48] the exact same result.
[01:55:50] Um
[01:55:52] and that's because this is in the
[01:55:53] identical model. Not only does it
[01:55:55] achieve the same loss, but um as I
[01:55:58] mentioned, these are identical models,
[01:55:59] and this W is the log counts of what
[01:56:02] we've estimated before. But, we came to
[01:56:05] this answer in a very different way and
[01:56:07] it's got a very different
[01:56:08] interpretation. But, fundamentally, this
[01:56:10] is basically the same model and gives
[01:56:11] the same samples here. And so,
[01:56:14] that's kind of cool. Okay, so we've
[01:56:16] actually covered a lot of ground. We
[01:56:18] introduced the bigram character-level
[01:56:20] language model.
[01:56:22] We saw how we can train the model, how
[01:56:24] we can sample from the model, and how we
[01:56:25] can evaluate the quality of the model
[01:56:27] using the negative log likelihood loss.
[01:56:30] And then we actually trained the model
[01:56:31] in two completely different ways that
[01:56:33] actually give the same result and the
[01:56:35] same model.
[01:56:36] In the first way, we just counted up the
[01:56:38] frequency of all the bigrams and
[01:56:40] normalized.
[01:56:41] In the second way, we used the uh
[01:56:44] negative log likelihood loss as a guide
[01:56:47] to optimizing the counts matrix
[01:56:50] uh or the counts array so that the loss
[01:56:52] is minimized in the in a gradient-based
[01:56:55] framework. And we saw that both of them
[01:56:56] give the same result.
[01:56:58] And um
[01:57:00] that's it.
[01:57:01] Now, the second one of these, the
[01:57:02] gradient base framework, is much more
[01:57:03] flexible. And right now, our neural
[01:57:06] network is super simple. We're taking a
[01:57:08] single previous character, and we're
[01:57:10] taking it through a single linear layer
[01:57:12] to calculate the logits.
[01:57:14] This is about to complexify. So, in the
[01:57:16] follow-up videos, we're going to be
[01:57:17] taking more and more of these
[01:57:19] characters,
[01:57:20] and we're going to be feeding them into
[01:57:21] a neural net.
[01:57:23] But, this neural net will still output
[01:57:24] the exact same thing. The neural net
[01:57:25] will output logits.
[01:57:28] And these logits will still be
[01:57:29] normalized in the exact same way, and
[01:57:30] all the loss and everything else in the
[01:57:32] gradient gradient base framework,
[01:57:33] everything stays identical.
[01:57:35] It's just that this neural net will now
[01:57:37] complexify all the way to transformers.
[01:57:40] So, that's going to be pretty awesome,
[01:57:42] and I'm looking forward to it. For now,
[01:57:44] bye.
