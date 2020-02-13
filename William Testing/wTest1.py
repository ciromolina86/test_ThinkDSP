from scipy.stats import norm, kurtosis
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.stats import kurtosis
import numpy as np

x = np.linspace(-5, 5, 100)
ax = plt.subplot()
dist_names = ['laplace', 'norm', 'uniform']

print (stats)

for dist_name in dist_names:
    if dist_name == 'uniform':
        dist = getattr(stats, dist_name)(loc=-2, scale=4)
    else:
        dist = getattr(stats, dist_name)
    print (dist)
    data = dist.rvs(size=1000)
    kur = kurtosis(data, fisher=True)
    y = dist.pdf(x)
    ax.plot(x, y, label="{}, {}".format(dist_name, round(kur, 3)))
    ax.legend()
plt.show()
