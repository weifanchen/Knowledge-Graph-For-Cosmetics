# INF558_project

### products
- sephora_skin_care_product.jl has 2382 products
- 15 duplicates, same product with same id, but having different product name
    > product_id = [2163400, 2057669, 1802677, 2161636, 2028397, 2196467, 2156925, 1973841, 1907229, 1765007, 1723873, 2231504, 2021897, 1764950, 2087047]
- 71 products without ingredients, are saved in product_wo_ingredient.jl
- web cosdna won't be able to process long text of ingredients
    > [p['product_id'] for p in product_list3 if p['ingredient_list']==[] and p["minicategory"]=="Value & Gift Sets"] = [2202505]

# 70 products p['ingredient_list']==[] 


# Reference 
- [THESE ARE THE SKINCARE INGREDIENTS YOU SHOULD NEVER MIX](https://www.beautybay.com/edited/skincare-ingredients-you-should-never-mix/)