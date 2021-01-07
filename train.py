from konlpy.tag import Okt
import tensorflow as tf
import numpy as np
import collections
import os

with open("joongang_01_07_1837.txt", "r", encoding="utf-8") as file:
    text=file.read()

okt=Okt()
text1 = text.replace('다.','다.<eos>')
text1 = text1.replace('죠.','죠.<eos>')
text1 = text1.replace('?','?<eos>')
text1 = text1.replace('요.','요<eos>')

#okt로 형태소 분할하고 빈도수 체크하기
tokken = okt.morphs(text1)
tokken = ' '.join(tokken)
tokken = tokken.replace('< eos >', '<eos>')

tokken=tokken.split(' ')
vocab=collections.Counter(tokken)

len(vocab) # 20788

new_vocab = {}
sparse_vocab = []
new_vocab['**unknown**']=0
for i,v in vocab.items():
    if v == 1:
        new_vocab['**unknown**'] += 1
        sparse_vocab.append(i)
    else :
        new_vocab[i] = v
len(new_vocab)

vocab_name=new_vocab.keys()
vocab_name=[i for i in vocab_name]

char2idx = {u:i for i, u in enumerate(vocab_name)}
idx2char = np.array(vocab_name) # 11760 ...11420

# 희소 단어 변경 **unknown** 변경
sparse_tokken = []
for c in tokken:
    if c in sparse_vocab:
        sparse_tokken.append('**unknown**')
    else:
        sparse_tokken.append(c)

text_as_int = np.array([char2idx[c] for c in sparse_tokken])
len(text_as_int) #254004 , 248223

print('{}----- 변환----->{}'.format(repr(sparse_tokken[150:185]), text_as_int[150:185]))

# 10 seq 로 분할
seq_length = 30
example_per_epoch = len(text_as_int)//seq_length # 50800


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_memory_growth(gpus[0], True)

    dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

    for i in dataset.take(5):
        print(i)
        print(idx2char[i.numpy()])

    sequence = dataset.batch(seq_length + 1, drop_remainder=True)

    for item in sequence.take(5):
        print(repr(''.join(idx2char[item.numpy()])))


    def split_input_target(chunk):
        input_text = chunk[:-1]
        target_text = chunk[1:]
        return input_text, target_text


    dataset = sequence.map(split_input_target)

    BATCH_SIZE = 256
    BUFFER_SIZE = 1000

    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)

    vocab_size = len(vocab_name)
    embedding_dim = 256
    rnn_units = 128

    def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                      batch_input_shape=[batch_size, None]),
            tf.keras.layers.LSTM(rnn_units,
                                 return_sequences=True,
                                 stateful=True,
                                 recurrent_initializer='glorot_uniform'),  # Xavier 초기화
            tf.keras.layers.Dense(vocab_size)  
        ])
        return model

    model = build_model(
        vocab_size=vocab_size,
        embedding_dim=embedding_dim,
        rnn_units=rnn_units,
        batch_size=BATCH_SIZE)

    def loss(labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    model.compile(optimizer='adam', loss=loss)
    # checkpoint directory
    checkpoint_dir = 'seq5_6'
    # checkpoinrt file name
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True)

    EPOCHS = 300
    history = model.fit(dataset, epochs=EPOCHS, callbacks=[checkpoint_callback])


  except RuntimeError as e:
    print(e)

tf.train.latest_checkpoint(checkpoint_dir)

model = build_model(vocab_size, embedding_dim, rnn_units, batch_size=1)

model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

model.build(tf.TensorShape([1, None]))

def generate_text(model, start_string):
  # 생성할 문자의 수
  num_generate = 40

  # 시작 문자열을 숫자로 변환(벡터화)
  input_eval = char2idx[start_string]
  input_eval = np.array(input_eval).reshape(1,1)

  # 결과를 저장할 빈 문자열
  text_generated = []

  # batch size == 1
  model.reset_states()
  not_word = ['**unknown**','<eos>','.<eos>','?<eos>']
  not_word_id = [char2idx[i] for i in not_word]
  for i in range(num_generate):
      predictions = model(input_eval)
      # 배치 차원 제거
      predictions = tf.squeeze(predictions, 0)

      predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

      if predicted_id == not_word_id[0]:
          continue
      if predicted_id in not_word_id[1:]:
          break
      # 예측된 단어를 이전 은닉 상태와 함께 다음 모델에 전달
      input_eval = tf.expand_dims([predicted_id], 0)

      text_generated.append(idx2char[predicted_id])

  return (start_string + ' '.join(text_generated))

generate_text(model,'코로나')
