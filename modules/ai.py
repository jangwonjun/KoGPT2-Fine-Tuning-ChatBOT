import torch
from transformers import PreTrainedTokenizerFast

Q_TKN = "<usr>"
A_TKN = "<sys>"
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'

koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK) 
model = torch.load('./static/model/test.pt')

print(model)
print("loading ai components successfully")


class WonJunAI:
    def __init__(self, p1="사람", p2="AI"):
        self.p1 = p1
        self.p2 = p2
    @torch.no_grad()
    def create_response(self, text):
        gen_text = ""
        while True:
            input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(Q_TKN + text + SENT + A_TKN + gen_text)).unsqueeze(dim=0)
            pred = model(input_ids)
            pred = pred.logits
            gen = koGPT2_TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().numpy().tolist())[-1]
            if gen == EOS:
                break
            gen_text += gen.replace("▁", " ")
        return gen_text
