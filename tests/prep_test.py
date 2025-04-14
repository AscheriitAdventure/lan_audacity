import pyvips
import os

# Image URLs for graph nodes
icons = {
    "router": "C:/Users/g.tronche/Documents/Python/lan_audacity/assets/affinity/svg/naked/router.svg",  # icons/router_black_144x144.png
    "switch": "C:/Users/g.tronche/Documents/Python/lan_audacity/assets/affinity/svg/naked/switch.svg",  # icons/switch_black_144x144.png
    "PC": "C:/Users/g.tronche/Documents/Python/lan_audacity/assets/affinity/svg/circle/blue/c_client_blue.svg"  # icons/computer_black_144x144.png
}

size: int = 144
for k, p in icons.items():
    c_f = pyvips.Image.thumbnail(p, size, height=size)
    n_f = f"{k}_{size}x{size}.png"
    o_p_j = os.path.join("C:","Users","g.tronche","Documents","Python","lan_audacity","assets","icons", n_f)
    c_f.write_to_file(o_p_j)
