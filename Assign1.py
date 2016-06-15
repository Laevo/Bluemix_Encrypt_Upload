import swiftclient
import keystoneclient
import gnupg
gpg = gnupg.GPG(gnupghome='CloudComp/gnupg', verbose = True)

#IBM Bluemix app Environment Variables.
auth_url = "https://identity.open.softlayer.com"
password = "c8kXuK8/~IHn(xe5"
project_id = "2fc86a6126e744eb846b440f3d76aaa2"
user_id = "eb1401b33c8b41d6aa134817b9cacde2"
username = "admin_924a9dda-94ca-4199-8dfc-80aade26e375_dbcfccf69ff9"
region_name = "dallas"
conn = swiftclient.Connection(key=password,
authurl=auth_url+'/v3',
auth_version='3',
user = username,
os_options = {
"project_id": project_id,
"user_id": user_id,
"region_name": region_name
})

container_name = 'pass_store'
file_name = 'Myfile.txt'

#Creating Container
conn.put_container(container_name)

#Encryption
##Creating RSA keys
input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, passphrase='iwbin', name_email='rohitvgaikwad@mavs.uta.edu')
key = gpg.gen_key(input_data)
##Encrypting file
with open(file_name, 'rb') as f:
    status = gpg.encrypt_file(f, 'rohitvgaikwad@mavs.uta.edu')

#Load file in Container
conn.put_object(container_name, file_name, contents=str(status), content_type='text/plain')

#Printing file details
for container in conn.get_account()[1]:
    for data in conn.get_container(container['name'])[1]:
        print 'object: {0}\t size: {1}\t date: {2}'.format(data['name'], data['bytes'], data['last_modified'])

# Download the file
obj = conn.get_object(container_name, file_name)
with open('output.txt', 'wb') as my_file:
    decrypted_data = gpg.decrypt(obj[1], passphrase='iwbin')
    my_file.write(str(decrypted_data))


