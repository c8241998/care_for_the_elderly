import torch
import torchvision
from torchvision import transforms
import PIL

class Emotion_classification:
    model = None
    transform = None
    device = "cuda" if torch.cuda.is_available() else "cpu"
    classes = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    @classmethod
    def inference(cls, img):
        if cls.model == None:
            cls.model = torch.load('model.pt').to(cls.device)
            cls.model.eval()

        if cls.transform == None:
            cls.transform = transforms.Compose([
                transforms.Grayscale(num_output_channels=3),
                transforms.Resize(224),
                transforms.ToTensor(),
            ])
        img = cls.transform(img).to(cls.device)
        pred = cls.model(img.unsqueeze(0))
        _, pred_ = torch.max(pred, 1)
        pred_ = pred_.cpu().item()
        return cls.get_label(pred_)

    @classmethod
    def get_label(cls, id):
        return cls.classes[id]