import torch
from torch import nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class EmotionModel:
    def __init__(
        self,
        *,
        model_name: str = "dlckdfuf141/korean-emotion-kluebert-v2",
        device: str = "cpu",
    ):
        self.device = torch.device(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name).to(
            self.device
        )
        self.softmax = nn.Softmax(dim=1)
        self.id2label = self.model.config.id2label

    async def predict(self, *, text: str) -> dict[str, object]:

        encoded = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        encoded = {k: v.to(self.device) for k, v in encoded.items()}

        with torch.no_grad():
            output = self.model(**encoded)
            logits = output.logits
            probabilities = self.softmax(logits).squeeze().cpu().tolist()

        predicted_idx = int(torch.argmax(logits))
        predicted_label = self.id2label[predicted_idx]

        return {
            "predicted": predicted_label,
            "probabilities": {
                self.id2label[i]: round(probabilities[i], 4)
                for i in range(len(probabilities))
            },
        }
