"""
conftest_mobile.py
Fixtures de pytest para inicializar Appium con capabilities de Android e iOS.
El fixture `mobile_driver` ejecuta cada test en ambas plataformas automáticamente.
"""

import pytest
from appium import webdriver as appium_driver
from appium.options import UiAutomator2Options, XCUITestOptions

APPIUM_SERVER = "http://localhost:4723"


@pytest.fixture(scope="function", params=["android", "ios"])
def mobile_driver(request):
    """
    Fixture parametrizado: lanza sesión Appium en Android (UIAutomator2)
    o iOS (XCUITest). Se destruye tras cada test.
    """
    platform = request.param

    if platform == "android":
        opts = UiAutomator2Options()
        opts.platform_name          = "Android"
        opts.platform_version       = "13"
        opts.device_name            = "Samsung Galaxy S23"
        opts.app                    = "/builds/mitienda-android.apk"
        opts.app_package            = "com.mitienda.app"
        opts.app_activity           = "com.mitienda.app.MainActivity"
        opts.auto_grant_permissions = True
        opts.no_reset               = False
        opts.new_command_timeout    = 60

    else:  # ios
        opts = XCUITestOptions()
        opts.platform_name       = "iOS"
        opts.platform_version    = "17.0"
        opts.device_name         = "iPhone 15 Pro"
        opts.app                 = "/builds/mitienda-ios.ipa"
        opts.bundle_id           = "com.mitienda.ios"
        opts.auto_accept_alerts  = True
        opts.new_command_timeout = 60

    d = appium_driver.Remote(APPIUM_SERVER, options=opts)
    d.implicitly_wait(8)
    yield d
    d.quit()
