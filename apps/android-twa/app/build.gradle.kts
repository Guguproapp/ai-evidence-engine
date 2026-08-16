plugins {
    id("com.android.application")
}

android {
    namespace = "com.gugupro.aievidence"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.gugupro.aievidence"
        minSdk = 23
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            signingConfig = null
        }
    }
}

dependencies {
    implementation("com.google.androidbrowserhelper:androidbrowserhelper:2.7.2")
}
