from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
async def hello_world():
        return {"message": "Hello, World!"}

@app.get("/healthz")
async def health_check():
        return {"status": "healthy"}

# added prime numbers calculator
@app.get("/primes/{n}")
async def get_primes(n: int):
    if n <= 0:
        raise HTTPException(status_code=400, detail="Parameter n must be a positive integer")
    
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    
    return {"count": n, "primes": primes}

