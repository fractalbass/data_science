import matplotlib.pyplot as plt
import pandas as pd

# Read the file
file_path = "./data/Training_Results.csv"
epochs = []
training_mse = []
testing_mse = []
df = pd.read_csv(file_path)
print(df.columns)
plt.plot(df['Epoch'], df['Train_MSE'], label='Training MSE')
plt.plot(df['Epoch'], df['Tes_MSE'], label='Testing MSE')
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.title('Training and Testing MSE')
plt.legend()
plt.show()
