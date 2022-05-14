import random

def gen_flatten_dict(
  quantityConfig,
):
  output = {}
  for trait_type in quantityConfig:
    quantity_dict = quantityConfig[trait_type]
    flatten_list = []
    for k, v in quantity_dict.items():
      flatten_list += [k] * v
    random.shuffle(flatten_list)
    output[trait_type] = flatten_list
  return output


def gen_output(
  flatten_dict,
  base_name,
  collection_description
):
  num_gen = len(list(flatten_dict.values())[0])
  trait_types = list(flatten_dict.keys())
  output = []
  for index in range(num_gen):
    attributes = []
    for t in trait_types:
      attributes.append({
        "trait_type": t,
        "value": flatten_dict[t][index]
      })
    metadata = {
      "name": f'{base_name}{index}',
      "description": collection_description, 
      "attributes": attributes
    }
    output.append(metadata)
  return output

# generate metadata from config
def gen_metadata(
  quantityConfig,
  base_name,
  collection_description
):
  flatten_dict = gen_flatten_dict(quantityConfig)
  output = gen_output(flatten_dict, base_name , collection_description)
  return output

def test():
  base_name = 'base_name'
  collection_description = 'collection_description'
  quanConInput = {
    'background': {
      "White": 10,
      "Black": 15,
    },
    'Body': {
      "thin": 20,
      "Black": 5,
    },
    'hat': {
      "large": 7,
      "small": 18,
    },
  }
  out = gen_metadata(quanConInput, base_name, collection_description)
  print(out)
# test()