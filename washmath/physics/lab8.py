def electric_force(velocity:Vector, magnetic_field:Vector, electric_field:Vector, charge:Fraction = Fraction(1)) -> Vector:
	"""
	Returns the total electric force
	:param washmath.classes.Vector velocity: A vector representing the velocity (v) of the charge [m/s].
	:param washmath.classes.Vector magnetic_field: A vector representing the magnetic field (B) of the charge [T].
	:param washmath.classes.Vector electric_field: A vector representing the electric field (E) of the charge [N/C].
	:param washmath.classes.Fraction charge: The charge of the particle [C].

	:runit: [N]
	"""
	base_vector = velocity.cross_product(magnetic_field) + electric_field
	return base_vector * charge
