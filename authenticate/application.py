from io import BytesIO
from torch import argmax, load
from torch import device as DEVICE
from torch.cuda import is_available
from torch.nn import Sequential, Linear, SELU, Dropout, LogSigmoid
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Resize
from torchvision.models import resnet50

LABELS = ['None', 'Meningioma', 'Glioma', 'Pitutary']

device = "cuda" if is_available() else "cpu"

resnet_model = resnet50(pretrained=True)

for param in resnet_model.parameters():
    param.requires_grad = True

n_inputs = resnet_model.fc.in_features
resnet_model.fc = Sequential(Linear(n_inputs, 2048),
                            SELU(),
                            Dropout(p=0.4),
                            Linear(2048, 2048),
                            SELU(),
                            Dropout(p=0.4),
                            Linear(2048, 4),
                            LogSigmoid())

for name, child in resnet_model.named_children():
    for name2, params in child.named_parameters():
        params.requires_grad = True

resnet_model.to('cpu')
resnet_model.load_state_dict(load('authenticate/model/bt_resnet50_model.pt', map_location=DEVICE('cpu')))
resnet_model.eval()

def preprocess_image(image_bytes):
  transform = Compose([Resize((512, 512)), ToTensor()])
  img = Image.open(BytesIO(image_bytes))
  return transform(img).unsqueeze(0)

def get_prediction(image_bytes):
  tensor = preprocess_image(image_bytes=image_bytes)
  y_hat = resnet_model(tensor.to('cpu'))
  class_id = argmax(y_hat.data, dim=1)
  return str(int(class_id)), LABELS[int(class_id)]

def predict(request,a):
  if request.method == 'POST':
    file1 = a
    img_bytes = file1.read()
    class_id, class_name = get_prediction(img_bytes)
    return {'class_id': class_id, 'class_name': class_name}

