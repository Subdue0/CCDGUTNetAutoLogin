include $(TOPDIR)/rules.mk

PKG_NAME:=python-autologin
PKG_RELEASE:=1.0
PKG_MAINTAINER:=Subdue<1374700812@qq.com>
PKG_BUILD_DIR := $(BUILD_DIR)/$(PKG_NAME)

include $(INCLUDE_DIR)/package.mk
define Package/$(PKG_NAME)
	SECTION:=lang-python
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=Automatically log in to the campus network(CCDGUT)
	DEPENDS:=+python +pillow
endef

define Package/$(PKG_NAME)/description
	This package contains a python script, the script can automatically log in to the campus network(CCDGUT).
endef

define Build/Prepare
	mkdir -p $(PKG_BUILD_DIR)
	$(CP) -R ./src/* $(PKG_BUILD_DIR)/
endef

define Build/Configure
endef

define Build/Compile
endef

define Package/$(PKG_NAME)/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/autologin $(1)/usr/sbin/autologin
endef

$(eval $(call BuildPackage,$(PKG_NAME)))
