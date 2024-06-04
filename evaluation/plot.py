import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('scores.csv')
print(data)

# Plot the data
plt.scatter(data['Batch1'], data['Batch2'])
plt.xlabel("Batch1")
plt.ylabel("Batch2")

# Save the plot
plt.savefig('scores.png')

# Show the plot
plt.show()
