import json
import requests
import pandas as pd
import numpy as np

url = "http://127.0.0.1:8000/graphql"

kueri = """
query {
    getBuyers{
    buyerId
    name
    email
    phone
    address}
}
"""

# 2: for get all data from vessels
kueri2 ="""
query {
    getVessels{
    vesselId
    name
    distributorId
    buyerId
    active}
}
"""

# 3: for get all data from catches
kueri3 ="""
query {
    getCatches{
    catchId
    vesselId
    localShopId
    productId
    creationDate}
}
"""

# 4: get all data from products
kueri4 ="""
query {
    getProducts{
    productId
    name
    quantity
    description
    priceProduct}
}
"""

# 5: for get all data from local shops
kueri5 ="""
query {
    getLocalShops{
    localShopId
    name
    location}
}
"""

# 6: for get all data from distributors
kueri6 ="""
query {
    getDistributors{
    distributorId
    resourceId
    name
    email
    phone}
}
"""

# 7: for get all data from resources
kueri7 ="""
query {
    getResource{
    resourceId
    name
    resourceType
    resourceDetails}
}
"""

header = {"Content-Type": "application/json"}

# Function to easier the process of sending request and auto print
def test_kueri(kueri_x: str, url_x:str, head: dict):
    responses = requests.post(url_x,
                              headers=head,
                              data=json.dumps({"query": kueri_x}))
    
    return responses.json()


tes_0 = requests.get("http://127.0.0.1:8000/buyers/search/?name=John Doe")
coba1 = tes_0.json()
print(f"Kueri untuk mengambil data buyer 'John Doe': \n {coba1}")



tes_1 = test_kueri(kueri, url, header)
df_1  = pd.DataFrame(tes_1['data']['getBuyers'])
df_1.to_csv("buyers.csv", index=False)

tes_2 = test_kueri(kueri2, url, header)
df_2  = pd.DataFrame(tes_2['data']['getVessels'])
df_2.to_csv("vessels.csv", index=False)

tes_3 = test_kueri(kueri3, url, header)
df_3  = pd.DataFrame(tes_3['data']['getCatches'])
df_3.to_csv("catches.csv", index=False)

tes_4 = test_kueri(kueri4, url, header)
df_4  = pd.DataFrame(tes_4['data']['getProducts'])
df_4.to_csv("products.csv", index=False)

tes_5 = test_kueri(kueri5, url, header)
df_5  = pd.DataFrame(tes_5['data']['getLocalShops'])
df_5.to_csv("local_shops.csv", index=False)

tes_6 = test_kueri(kueri6, url, header)
df_6  = pd.DataFrame(tes_6['data']['getDistributors'])
df_6.to_csv("distributors.csv", index=False)

tes_7 = test_kueri(kueri7, url, header)
df_7  = pd.DataFrame(tes_7['data']['getResource'])
df_7.to_csv("resources.csv", index=False)



# Output:
# {'data': {'getBuyers': [{'buyerId': 1, 'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '123-456-7890', 'address': '123 Ocean Avenue'}, {'buyerId': 2, 'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'phone': '321-654-0987', 'address': '456 Sea Breeze Blvd'}, {'buyerId': 3, 'name': 'Alice Brown', 'email': 'alice.brown@example.com', 'phone': '654-321-0987', 'address': '789 Bay Street'}]}}