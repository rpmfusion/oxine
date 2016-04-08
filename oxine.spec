Summary: Lightweight, purely OSD based xine frontend
Name: oxine
Version: 0.7.1
Release: 24%{?dist}
License: GPLv2+
Group: Applications/Multimedia
URL: http://oxine.sourceforge.net/
Source0: http://downloads.sf.net/oxine/oxine-%{version}.tar.gz
Source1: oxine.desktop
Source2: oxine.png
Patch0: oxine-strptime.patch
Patch1: oxine-0.7.1-fix-inline-use.patch
# We need xineplug_decode_image.so for the backgrounds
Requires: xine-lib-extras
BuildRequires: libX11-devel, libXtst-devel, libXinerama-devel
Buildrequires: gettext
BuildRequires: xine-lib-devel >= 1.0.1
BuildRequires: curl-devel
BuildRequires: ImageMagick-devel
BuildRequires: lirc-devel
BuildRequires: desktop-file-utils
BuildRequires: dbus-glib-devel
BuildRequires: libexif-devel
BuildRequires: libcdio-devel
BuildRequires: gtk2-devel
# The build fails (0.7.0) if cdparanoia isn't found
Buildrequires: cdparanoia, vorbis-tools

%description
oxine is a lightweight gui for the famous xine engine which uses the on screen
display functionality of xine to display its user interface elements like
buttons, lists sliders and so on. Due to this, oxine can easily be ported to
any video output device the xine library provides (e.g. frame buffer, dxr3,...)
and is particularly suitable for appliances like set-top boxes, home
entertainment systems or kiosk systems.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Convert file to utf-8 (still as of 0.7.1)
for file in AUTHORS; do
    iconv -f iso8859-1 -t utf-8 -o tmp ${file}
    touch -r ${file} tmp
    mv -f tmp ${file}
done
rm -f tmp


%build
# --without-jsw until we get libjsw packaged, but that won't be very easy
%configure \
    --enable-vdr \
    --without-jsw
make %{?_smp_mflags}


%install
%make_install
%find_lang %{name}

# Desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
# This is the image we'll use for the desktop icon. Could be improved.
# (based on data/skins/oxinetic/backgrounds/icon-cdrom.png)
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/oxine.png


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%doc doc/keymapping.pdf doc/README.html
%{_bindir}/oxine
%{_datadir}/applications/oxine.desktop
%{_datadir}/icons/hicolor/64x64/apps/oxine.png
%{_datadir}/oxine/


%changelog
* Fri Apr 08 2016 Adrian Reber <adrian@lisas.de> - 0.7.1-24
- remove BR: mdsplib-devel; package retired in F24

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 0.7.1-23
- Fix FTBFS (rf#3628)
- Modernize spec

* Sun Aug 03 2014 Sérgio Basto <sergio@serjux.com> - 0.7.1-22
- Rebuilt for new ImageMagick.

* Tue Mar 25 2014 Xavier Bachelot <xavier@bachelot.org> - 0.7.1-21
- Rebuild for libcdio 0.92.
 
* Wed Oct 23 2013 Xavier Bachelot <xavier@bachelot.org> - 0.7.1-20
- Rebuild for xine-lib 1.2.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 30 2013 Kevin Fenzi <kevin@scrye.com> - 0.7.1-18
- Rebuild for broken deps in rawhide

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Adrian Reber <adrian@lisas.de> 0.7.1-16
- Rebuild for libcdio-0.90

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 29 2012 Matthias Saou <matthias@saou.eu> 0.7.1-14
- Rebuild for new ImageMagick.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 20 2011 Adrian Reber <adrian@lisas.de> 0.7.1-12
- Rebuild for libcdio-0.83

* Tue Apr 26 2011 Matthias Saou <http://freshrpms.net/> 0.7.1-11
- Rebuild with hal disabled : hal is dead, obsoleted by udev.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.7.1-9
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Dan Horák <dan[at]danny.cz> 0.7.1-8
- drop the BR: eject as it doesn't exist on all platforms, direct ioctl call is used instead,
  also a corresponding R: was missing

* Mon Sep 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> 0.7.1-7
- rebuild for new ImageMagick

* Fri Jan 22 2010 Adrian Reber <adrian@lisas.de> 0.7.1-6
- Rebuild for libcdio-0.82
- Added patch for "error: implicit declaration of function 'strptime'"

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 11 2009 Matthias Saou <http://freshrpms.net/> 0.7.1-4
- Rebuild for new ImageMagick.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 13 2009 Adrian Reber <adrian@lisas.de> 0.7.1-2
- Rebuild for libcdio-0.81

* Tue May 13 2008 Matthias Saou <http://freshrpms.net/> 0.7.1-1
- Update to 0.7.1.
- Convert AUTHORS file to utf-8.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Thu Aug 30 2007 Matthias Saou <http://freshrpms.net/> 0.7.0-1
- Update to 0.7.0.
- Add new build requirements.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-6
- Rebuild for new BuildID feature.

* Wed Aug  8 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-5
- Include patch to pass (now mandatory) mode to O_CREAT open call.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-4
- Update License field.

* Fri Jun 15 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-3
- Include desktop entry and icon based on a CD image from the default theme.

* Fri May 11 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-2
- Fix black screen problem by requiring xine-lib-extras, where
  xineplug_decode_image.so is available.

* Thu May 10 2007 Matthias Saou <http://freshrpms.net/> 0.6.6-1
- Update to 0.6.6 by including the official patch (no full sources available).
- Remove no longer needed (and possibly incorrect anyway) install patch.

* Tue May  8 2007 Matthias Saou <http://freshrpms.net/> 0.6-2
- Enable weather now that mdsplib is built.

* Mon Dec 18 2006 Matthias Saou <http://freshrpms.net/> 0.6-1
- Update to 0.6.
- Include install patch.
- Enable VDR.
- Disable (at least for now) weather and jsw because of not-yet-packaged libs.

* Wed Aug 31 2005 Matthias Saou <http://freshrpms.net/> 0.3.5-0.1.cvs
- Update to CVS snapshot.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.2-3.fr
- Rebuild for Fedora Core 1.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Mon Mar 24 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.2.

* Tue Mar 18 2003 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

