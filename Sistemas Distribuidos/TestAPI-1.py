import requests
import imageio.v2 as iio
import matplotlib.pyplot as plt

url = "https://jsonplaceholder.typicode.com/users/"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    #print(data)
    for i,d in enumerate(data) :
        print(f"{i}: {d}")
    #print("Nombre:", data["name"])
    #print("Email:", data["email"])
else:
    print("Error:", response.status_code)

#img = iio.imread("g4g.png")
#plt.imshow(img)
#plt.show()