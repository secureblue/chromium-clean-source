%global numjobs %{_smp_build_ncpus}

Source0: chromium-version.txt

Name:	 trivalent-chromium-clean-source
%{lua:
       local f = io.open(macros['_sourcedir']..'/chromium-version.txt', 'r')
       local content = f:read "*all"
       print("Version: "..content.."\nRelease: "..os.time().."\n")
}
Summary: Chromium's source tarball.
Url:     http://www.chromium.org/Home
License: BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)

BuildRequires: git
BuildRequires: python3

%description
Vanilla chromium source, cleaned to reduce size and some proprietary bits.

%build
# obtain cleaning utilities
git clone https://github.com/secureblue/trivalent-chromium-clean-source.git
cp trivalent-chromium-clean-source/* .

# obtain depot tools for obtaining source
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH="$(pwd)/depot_tools:$PATH"
mkdir chromium
cp ffmpeg-clean.patch chromium/
cd chromium

# obtain source, specific version of source, and needed deps (hooks)
fetch --nohooks --no-history chromium
cd src
git fetch origin refs/tags/%{version}:refs/tags/%{version}
git checkout %{version}
gclient runhooks
gclient sync -D

# clean
rm -rf ./build/linux/debian_bullseye_amd64-sysroot ./build/linux/debian_bullseye_i386-sysroot ./third_party/node/linux/node-linux-x64 ./third_party/rust-toolchain ./third_party/rust-src
chmod a+rx ./../../clean_ffmpeg.sh ./../../get_free_ffmpeg_source_files.py
cp ./../../get_free_ffmpeg_source_files.py ./
./../../clean_ffmpeg.sh . 0
rm ./get_free_ffmpeg_source_files.py
find ./third_party/openh264/src -type f -not -name '*.h' -delete

# extra clean
rm -rf ./media/test/data ./third_party/jdk/current ./third_party/liblouis/src/tests/braille-specs \
       ./third_party/blink/web_tests ./third_party/catapult/tracing/test_data ./third_party/depot_tools/.cipd_bin

# compress
cd ..
mv src/ chromium-%{version}/
tar --exclude=\\.git -cf - chromium-%{version} | xz -9 -M 90% -T %{numjobs} -f > chromium-%{version}-clean.tar.xz
mv chromium-%{version}-clean.tar.xz ./../

%install
mkdir -p %{buildroot}%{_usrsrc}/chromium/
install -m 0644 chromium-%{version}-clean.tar.xz %{buildroot}%{_usrsrc}/chromium/

%files
%{_usrsrc}/chromium/chromium-%{version}-clean.tar.xz
