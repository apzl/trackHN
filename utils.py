import torch
from scipy.spatial.distance import cosine

def highlight(sim):
  r = 245
  g = (129*(sim-0.8)/-0.4)+4
  b = (82*(sim-0.8)/-0.4)+88
  return r,g,b

def word_embed(text, word, model, tokenizer):
  marked_text = "[CLS] " + text + " [SEP]"
  tokenized_text = tokenizer.tokenize(marked_text)
  indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
  segments_ids = [1] * len(tokenized_text)
  tokens_tensor = torch.tensor([indexed_tokens])
  segments_tensors = torch.tensor([segments_ids])
  model.eval()
  with torch.no_grad():
    outputs = model(tokens_tensor, segments_tensors)
    hidden_states = outputs[2]
  token_embeddings = torch.stack(hidden_states, dim=0)
  token_embeddings = torch.squeeze(token_embeddings, dim=1)
  token_embeddings = token_embeddings.permute(1,0,2)
  token_vecs_sum = []
  index = 0
  for token in token_embeddings:
    sum_vec = torch.sum(token[-4:], dim=0)
    token_vecs_sum.append(sum_vec)
  for i, token_str in enumerate(tokenized_text):
    if (token_str == word):
      index=i
    
  return token_vecs_sum[index]








