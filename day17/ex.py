# Find highest positive y velocity that gets us into the rectangle
# having the following bounding coordinates

# %%
# target area: x=137..171, y=-98..-73
x1, x2 = (137, 171)  # inclusive
y1, y2 = (-98, -73)

#x1,x2=(20,30)
#y1,y2=(-10,-5)

# Let's find the starting velocity `vx` range.
# Upper bound is overshooting `x2` in the first step.
# Lower bound is when 1+2+...+vx = x1
# or vx*(vx+1)/2 < x1 ==> vx^2+vx-2*x1 = 0
# vx = (-1 + sqrt(1 + 8*x1))/2

assert(x1 > 0)
vx_upper_bound = x2  # single step
vx_lower_bound = int((np.sqrt(1 + 8*x1)-1)/2)  # also min number of steps

# Let's take care of Y coordinate.
# Suppose as an example that dy_0 = 4. We'll get
# 4, 7, 9, 10, 10, 9, 7, 4, 0, -5, ...
# So, after 2*dy_0+1 steps we're back to y=0 with dy=-dy_0-1
# So: dy_0 = dy+1 when back at y=0, and dy <= y1 in order not to overshoot in one step
# ==> dy_0 <= -y1+1

vy_lower_bound = y1-1
vy_upper_bound = -y1+2

# %%
def simulate(dx, dy, x1, x2, y1, y2):
    x, y = (0, 0)
    while True:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        if x > x2 or y < y1:
            return False
        x += dx
        y += dy
        dx = dx-1 if dx > 0 else 0
        dy = dy-1
# %%
best_dy = -1000000
best_dx = 0
num_solutions = 0
for dx in range(vx_lower_bound, vx_upper_bound+1):
    for dy in range(vy_upper_bound, vy_lower_bound-1, -1):
        if simulate(dx, dy, x1, x2, y1, y2):
            num_solutions += 1
            if dy > best_dy:
                best_dx, best_dy = dx, dy
                best_dy = dy
            # break   # commented due to part 2
max_height = best_dy * (best_dy+1) // 2
assert(best_dy > 0)
print('Best dx,dy:',best_dx, best_dy)
print('Max height (part 1):', max_height)
print('Number of solutions (part 2):', num_solutions)
# %%
