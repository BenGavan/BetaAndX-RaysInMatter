import matplotlib.pyplot as plt
import numpy as np

# Plot data
x = np.linspace(0,1,100)
y = x**2
fig = plt.figure()
ax = fig.add_subplot(221) #small subplot to show how the legend has moved.

# Create legend
plt.plot(x, y, label = '{\\footnotesize \$y = x^2\$}')
leg = plt.legend( loc = 'upper right')

plt.draw() # Draw the figure so you can find the positon of the legend.

# Get the bounding box of the original legend
bb = leg.get_bbox_to_anchor().inverse_transformed(ax.transAxes)

# Change to location of the legend.
xOffset = 0
bb.x0 += xOffset
bb.x1 += xOffset
leg.set_bbox_to_anchor(bb, transform = ax.transAxes)


# Update the plot
plt.show()