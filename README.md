# ClassicalMusicComposer
A Neural Network which composes the notes for Indian Classic Music

#MUSIC GENERATION WITH LSTM NETWORKS

## 1. Why lstm networks?
To start off, the type of neural network I used was a recurrent neural network. The recurrent neural network was trained and provided inputs and gave satisfactory outputs. But, recurrent neural networks suffer from a problem in which it does not remember adequate number of previous inputs. This is a problem in song generation as the network forgets the entire music structure of the song and considers only the last few notes. This is problem is known as vanishing gradients. This is the reason why LSTM networks offer better capability.
To read more on why LSTM offer more than recurrent, read the introduction of the following [paper](http://people.idsia.ch/~juergen/blues/IDSIA-07-02.pdf).
## 2. Assumptions Made
There is an underlying pattern to every note present in any song by the same composer. If presented with enough training sets the neural network can pick up on that pattern and use it for notes prediction.
As of now I have only considered and made predictions considering the swaras S,R,G,M,P,D,N. I am looking for input as to whether I should add - , . etc.
I consider the higher and lower tones to be the same as they do not make a difference in the music generated. For example, I consider the higher S and the lower S to be the same as they do not affect the lyric of the song as a whole just the way it is sung. Hence, I do not feel a need to add the tones of the swaras as a factor the neural network should have to consider.
## 3. How it works
The code contains of first constructing a data set which is sequential. Sequential data set map one note to the next and are capable of holding sequences. After inserting the training data into sequential data set the neural network has been constructed as follows-
   -Input Layer – The input layer has only one node since the network has only one set of parameters to consider while constructing the next i.e. the previous notes.
   -Hidden Layer – The Hidden Layer’s number of nodes has been got through trial and error by changing the number of nodes and seeing how efficient the prediction is. After examining values of hidden layer from 3-100 the error rate was minimum for 8 nodes.
  -Output Layer – The Output Layer’s number of nodes is one. When a neural network is outputting a value instead of true or false the number of output nodes used is generally one.

After everything has been set, the training phase is done by using an Reverse Propagation Trainer. 

## 4. Libraries used for lstm
The library used to construct the LSTM networks is called pybrain, a python based library. Here’s a link to the documentation of [pybrain](http://pybrain.org/docs/).

