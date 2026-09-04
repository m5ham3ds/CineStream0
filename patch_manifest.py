import re
with open('app/src/main/AndroidManifest.xml', 'r') as f:
    content = f.read()

# Make sure INTERNET permission is there
if 'android.permission.INTERNET' not in content:
    content = content.replace('<application', '<uses-permission android:name="android.permission.INTERNET" />\n    <application')

if 'android:usesCleartextTraffic="true"' not in content:
    content = content.replace('<application', '<application android:usesCleartextTraffic="true"')

with open('app/src/main/AndroidManifest.xml', 'w') as f:
    f.write(content)
