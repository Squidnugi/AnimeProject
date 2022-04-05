# import generate_password_hash and check_password_hash here:
from werkzeug.security import check_password_hash, generate_password_hash

hardcoded_password_string = "123456789_bad_password"

# generate a hash of hardcoded_password_string here:

hashed_password = generate_password_hash(hardcoded_password_string)
print(hashed_password)

password_attempt_one = "abcdefghij_123456789"

# check password_attempt_one against hashed_password here:

hash_match_one = check_password_hash(password_attempt_one, hashed_password)
print(hash_match_one)

password_attempt_two = "123456789_bad_password"

# check password_attempt_two against hashed_password here:

hash_match_two = check_password_hash(hashed_password, password_attempt_two)
print(hash_match_two)

hash = generate_password_hash('Squidnugi')

print(check_password_hash(hash, 'Squidnugi1'))