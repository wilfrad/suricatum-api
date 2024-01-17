from contents.content import init_builder, get_testimonials_contents, get_suricatum_tv_contents

init_builder()

print(get_testimonials_contents()[0].contents[0].images.profile_photo)
print(get_suricatum_tv_contents()[0].contents[0].images.content_cover)