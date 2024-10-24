from tokens import get_entry,gen_token,add_entry,remove_entry


t1 = add_entry()
t2 = add_entry()
t3 = add_entry()

print(get_entry(t1))
remove_entry(t1)
print(get_entry(t2))
print(get_entry(t3))
print(get_entry("null"))
