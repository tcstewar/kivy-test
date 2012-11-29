labels=dict(
    x0='starting prey population',
    y0='starting predator population',
    b='prey growth',
    p='predator impact',
    d='predator death rate',
    r='predator growth rate',
    )

ranges=dict(
    x0=(0, 2),
    y0=(0, 2),
    b=(0, 2),
    p=(0, 2),
    r=(0, 2),
    d=(0, 2),
    )

colors=dict(
    x=0,
    y=0.7,
    )
    

def model(x0=1.0, y0=0.1, b=1.0, p=1.0, r=1.0, d=1.0, T=30, dt=0.01):
    t=0
    xs=[]
    ys=[]
    x=x0
    y=y0
    while t<T:
        f = b - p*y
        g = r*x - d
        x += x*f*dt
        y += y*g*dt
        if x<0: x = 0
        if y<0: y = 0
        
        xs.append(x)
        ys.append(y)
        t+=dt
        
    return dict(x=xs, y=ys)    
    
        
    
