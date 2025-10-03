import requests
import imageio.v2 as iio
import matplotlib.pyplot as plt

url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Nombre:", data["name"])
    print("Email:", data["email"])
else:
    print("Error:", response.status_code)




img = iio.imread("g4g.png")

plt.imshow(img)
plt.show()