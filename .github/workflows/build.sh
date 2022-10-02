pip install git+https://github.com/abdnh/ankibuild@5092188f6b7c73e7bab2c7f64e7008a7e24466f6#egg=ankibuild[qt5,qt6]

# Build zstandard from source to work around "C API versions mismatch" error
git clone https://github.com/indygreg/python-zstandard
cd python-zstandard
git checkout 6006fdf164ac0e89b260706a3e4ef5806aceffb6
cd ..
pip install ./python-zstandard/ -t src/vendor

pip install -U git+https://github.com/abdnh/zimply-core@eddf548b778d9046020ba84d9912257d1cb949fb -t src/vendor

make
