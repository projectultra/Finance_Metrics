import keras
import tensorflow
import numpy as np
inp=np.array([231,230.85001,230.87,4.83,0.79,4.985,5.,5.])
model=keras.models.load_model(r'META/METAmodel')
inp=inp.astype(np.float64)
inp=inp.reshape(1,8)
pred=model.predict(inp)
print(pred)