import cmath
import math

# 1) Complex numbers
z1 = 3 + 4j
z2 = complex(0, -2)
print("1) Complex numbers:")
print(f"z1 = {z1}, z2 = {z2}")

# 3) Magnitude (modulus) and argument
modulus = abs(z1)
argument = cmath.phase(z1)
print("\n3) Magnitude and argument:")
print(f"|z1| = {modulus}")
print(f"arg(z1) = {argument} rad")

# 4) Polar form and Euler's formula
r, theta = cmath.polar(z1)
print("\n4) Polar form:")
print(f"Polar form: r = {r}, theta = {theta} rad")
print(f"z1 = r(cosθ + i sinθ) = {r} * (cos({theta}) + i*sin({theta}))")
print(f"Euler form: z1 = {cmath.rect(r, theta)}")
print(f"e^(iθ) = {cmath.exp(1j * theta)}")

# 5) Complex arithmetic and powers
sum_z = z1 + z2
product_z = z1 * z2
quotient_z = z1 / z2
power_z = z1 ** 2
print("\n5) Arithmetic and powers:")
print(f"z1 + z2 = {sum_z}")
print(f"z1 * z2 = {product_z}")
print(f"z1 / z2 = {quotient_z}")
print(f"z1^2 = {power_z}")

# Extra: De Moivre's theorem example
angle = cmath.phase(z1)
print("\nDe Moivre check:")
print(f"(cosθ + i sinθ)^3 = {cmath.exp(1j * 3 * angle)}")
