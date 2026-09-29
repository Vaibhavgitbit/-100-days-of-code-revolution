The Old Way (Bulk RAM Sponge):
extracted_products.append(product_entry) 

with open("clean_products.json", "w") as f:
    json.dump(extracted_products, f)

----------------------------------------
New way :
#  Saving instantly to disk, keeping RAM flat at zero
with open("clean_products.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(product_entry) + "\n")
    
