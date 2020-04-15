# INF558_project

## Outputs
 1. The original product list: **sephora_skincare_product.jl**
    * #2386
    * 15 duplicates, same product with same id, but having different product name
        *  product_id = [2163400, 2057669, 1802677, 2161636, 
        2028397, 2196467, 2156925, 1973841, 1907229, 1765007, 1723873, 2231504, 2021897, 1764950, 2087047]
    * 56 products have no ingredients

 2. based on the original product list to simplify the ingredient text: **sephora_skincare_product_revised.jl**
    * because cosdna is not able to process long text of ingredients
        * [p['product_id'] for p in product_list3 if p['ingredient_list']==[] and p["minicategory"]=="Value & Gift Sets"] = [2202505]
    * #2382
    * 71 products have no ingredients

 3. base on simplified ingredient text to generate ingredient list: **sephora_skincare_product_ingredient_list.jl**
    * #2384
    * 73 products have no ingredients, are saved in product_wo_ingredient.jl
    * 78 products have empty ingredient list

 4. **ingredients.jl**

 5. 


## Reference 
- [THESE ARE THE SKINCARE INGREDIENTS YOU SHOULD NEVER MIX](https://www.beautybay.com/edited/skincare-ingredients-you-should-never-mix/)

- [FDA-Allergens in Cosmetics](https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics)
