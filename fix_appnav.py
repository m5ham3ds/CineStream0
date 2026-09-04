with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    lines = f.readlines()

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    for line in lines:
        if "updateFinishedShowGreen" not in line and "isUpdatingData" not in line and "BackgroundWebView" not in line and "SiteVerificationManager" not in line:
            f.write(line)
