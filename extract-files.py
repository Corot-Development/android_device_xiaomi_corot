#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

_displayservice_ping = (
    b'_ZN7lineage10frameworks14displayservice4V1_014IEventCallback4pingEv'
)
_displayservice_unresolved = (
    rb'_ZN7lineage10frameworks14displayservice4V1_01[45]I[A-Za-z0-9_]*'
    rb'(?:linkToDeath|unlinkToDeath|getDebugInfo|getHashChain|'
    rb'interfaceChain|interfaceDescriptor|5debug|registerForNotifications)'
    rb'[A-Za-z0-9_]*'
)
_displayservice_ctor_vtable = (
    rb'_ZTCN[A-Za-z0-9_]+E\d+_'
    rb'N7lineage10frameworks14displayservice4V1_01[45]I[A-Za-z0-9_]*E'
)

namespace_imports = [
    'device/xiaomi/corot',
    'hardware/mediatek',
    'hardware/mediatek/libion_mtk',
    'hardware/mediatek/libmtkperf_client',
    'hardware/xiaomi',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'odm/lib64/libmt_mitee@1.3.so': blob_fixup()
        .replace_needed('android.hardware.security.keymint-V2-ndk.so', 'android.hardware.security.keymint-V4-ndk-v34.so')
        .replace_needed('libkeymint_support.so', 'libkeymint_support_V4.so'),

    ('vendor/etc/init/android.hardware.neuralnetworks-shim-service-mtk.rc'): blob_fixup()
        .regex_replace('start', 'enable'),

    'vendor/bin/hw/android.hardware.graphics.composer@3.1-service': blob_fixup()
        .replace_needed('android.hardware.graphics.composer@2.1-resources.so', 'android.hardware.graphics.composer@2.1-resources-v34.so'),

    'vendor/bin/hw/android.hardware.security.keymint@2.0-service.mitee': blob_fixup()
        .replace_needed('android.hardware.security.keymint-V2-ndk.so', 'android.hardware.security.keymint-V4-ndk-v34.so')
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),

    'vendor/firmware/txpowerctrl.cfg': blob_fixup()
        .regex_replace('\t', ''),

    'vendor/bin/hw/mtkfusionrild' : blob_fixup()
        .add_needed('libutils-v32.so'),

    'vendor/etc/vintf/manifest/manifest_media_c2_V1_2_default.xml': blob_fixup()
        .regex_replace('1.1', '1.2'),

    'vendor/lib64/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libalsautils.so', 'libalsautils-v33.so'),

    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),

    ('vendor/bin/mnld', 'vendor/lib64/mt6985/libaalservice.so', 'vendor/lib64/mt6985/libpqconfig.so', 'vendor/lib64/librgbwlightsensor.so'): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'android.hardware.sensors@1.0-convert-shared.so')
        .replace_needed('libmnl.so', 'libmnl_mtk.so'),

    ('vendor/lib64/libalLDC.so', 'vendor/lib64/libalAILDC.so', 'vendor/lib64/libalhLDC.so'): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    ('vendor/lib64/hw/hwcomposer.mtk_common.so', 'vendor/lib64/libmialgoengine.so', 'vendor/lib64/mt6985/lib3a.af.assist.so', 'vendor/lib64/mt6985/libcam.hal3a.so', 'vendor/lib64/mt6985/libcam.hal3a.ctrl.so', 'vendor/lib64/mt6985/libmtkcam_cputrack.so', 'vendor/lib64/mt6985/libmtkcam_request_requlator.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),

    'vendor/lib64/mt6985/libneuralnetworks_sl_driver_mtk_prebuilt.so': blob_fixup()
         .clear_symbol_version('AHardwareBuffer_allocate')
         .clear_symbol_version('AHardwareBuffer_createFromHandle')
         .clear_symbol_version('AHardwareBuffer_describe')
         .clear_symbol_version('AHardwareBuffer_getNativeHandle')
         .clear_symbol_version('AHardwareBuffer_lock')
         .clear_symbol_version('AHardwareBuffer_release')
         .clear_symbol_version('AHardwareBuffer_unlock'),

    ('vendor/lib64/libcodec2_vpp_AIMEMC_plugin.so', 'vendor/lib64/libcodec2_vpp_AISR_plugin.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.allocator-V1-ndk.so', 'android.hardware.graphics.allocator-V2-ndk.so')
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),

    ('vendor/lib64/vendor.mediatek.hardware.pq_aidl-V1-ndk.so', 'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V2-ndk.so', 'vendor/lib64/vendor.mediatek.hardware.pq_aidl-V3-ndk.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/bin/hw/android.hardware.neuralnetworks-shim-service-mtk', 'vendor/lib64/libnvram.so', 'vendor/lib64/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed('libformatter.so', 'libformatter_mtk.so'),


('vendor/bin/hw/android.hardware.gnss-service.mediatek',
	'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so'): blob_fixup()
    .replace_needed('android.hardware.gnss-V1-ndk_platform.so','android.hardware.gnss-V1-ndk.so'),

('vendor/lib64/mt6985/lib3a.flash.so',
     'vendor/lib64/mt6985/lib3a.sensors.color.so',
     'vendor/lib64/mt6985/lib3a.sensors.flicker.so'): blob_fixup()
        .add_needed('liblog.so'),

'vendor/lib64/hw/sensors.mediatek.V2.0.so': blob_fixup()
       .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so'),

('vendor/lib64/libcodec2_mtk_c2store.so', 'vendor/lib64/libcodec2_vpp_gc_plugin.so', 'vendor/lib64/libcodec2_vpp_qt_plugin.so', 'vendor/lib64/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v31.so'),

'vendor/lib64/libdolbyplugin.so': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libui.so', 'libui-v32.so'),

'vendor/lib64/mt6985/libmtkcam_hal_android_app_cbadaptor.so': blob_fixup()
        .replace_needed('android.frameworks.displayservice@1.0.so',
                        'lineage.frameworks.displayservice@1.0.so')
        .binary_regex_replace(
            b'7android10frameworks14displayservice',
            b'7lineage10frameworks14displayservice')
        .binary_regex_replace(
            _displayservice_unresolved,
            lambda m: _displayservice_ping.ljust(len(m.group(0)), b'\x00'))
        .binary_regex_replace(
            _displayservice_ctor_vtable,
            lambda m: _displayservice_ping.ljust(len(m.group(0)), b'\x00')),

('vendor/lib64/mt6985/libmtkcam_stdutils.so',
     'vendor/lib64/hw/mt6985/android.hardware.camera.provider@2.6-impl-mediatek.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),

'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),

('vendor/etc/libnfc-nxp.conf'): blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace('NFC_DEBUG_ENABLED=1', 'NFC_DEBUG_ENABLED=0'),

'vendor/bin/mi_thermald': blob_fixup()
        .binary_regex_replace(b'%d/on', b'%d/..'),

'vendor/etc/public.libraries.txt': blob_fixup()
        .add_line_if_missing('libmpbase.so'),

('vendor/lib64/libcodec2_mtk_vdec.so', 'vendor/lib64/libcodec2_mtk_venc.so', 'vendor/lib64/libcodec2_vpp_dolby_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so'),


'vendor/lib/hw/audio.primary.mediatek.so': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libalsautils.so', 'libalsautils-v33.so'),

('vendor/lib/hw/hwcomposer.mtk_common.so', 'vendor/lib/libmialgoengine.so', 'vendor/lib/mt6985/lib3a.af.assist.so', 'vendor/lib/mt6985/libcam.hal3a.so', 'vendor/lib/mt6985/libcam.hal3a.ctrl.so', 'vendor/lib/mt6985/libmtkcam_cputrack.so', 'vendor/lib/mt6985/libmtkcam_request_requlator.so'): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),

'vendor/lib/mt6985/libneuralnetworks_sl_driver_mtk_prebuilt.so': blob_fixup()
         .clear_symbol_version('AHardwareBuffer_allocate')
         .clear_symbol_version('AHardwareBuffer_createFromHandle')
         .clear_symbol_version('AHardwareBuffer_describe')
         .clear_symbol_version('AHardwareBuffer_getNativeHandle')
         .clear_symbol_version('AHardwareBuffer_lock')
         .clear_symbol_version('AHardwareBuffer_release')
         .clear_symbol_version('AHardwareBuffer_unlock'),

('vendor/lib/vendor.mediatek.hardware.pq_aidl-V1-ndk.so', 'vendor/lib/vendor.mediatek.hardware.pq_aidl-V2-ndk.so', 'vendor/lib/vendor.mediatek.hardware.pq_aidl-V3-ndk.so'): blob_fixup()
        .replace_needed('android.hardware.graphics.common-V3-ndk.so', 'android.hardware.graphics.common-V7-ndk.so'),
    ('vendor/bin/hw/android.hardware.neuralnetworks-shim-service-mtk', 'vendor/lib/libnvram.so', 'vendor/lib/libtflite_mtk.so'): blob_fixup()
        .add_needed('libbase_shim.so'),
    ('vendor/lib/libcodec2_mtk_vdec.so', 'vendor/lib/libcodec2_mtk_venc.so'): blob_fixup()
        .replace_needed('libformatter.so', 'libformatter_mtk.so'),

('vendor/lib/mt6985/lib3a.flash.so',
     'vendor/lib/mt6985/lib3a.sensors.color.so',
     'vendor/lib/mt6985/lib3a.sensors.flicker.so'): blob_fixup()
        .add_needed('liblog.so'),

('vendor/lib/libcodec2_mtk_c2store.so', 'vendor/lib/libcodec2_vpp_gc_plugin.so', 'vendor/lib/libcodec2_vpp_qt_plugin.so', 'vendor/lib/libcodec2_vpp_rs_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libsfplugin_ccodec_utils.so', 'libsfplugin_ccodec_utils-v31.so'),

'vendor/lib/libdolbyplugin.so': blob_fixup()
        .replace_needed('libcodec2_hidl@1.0.so', 'libcodec2_hidl@1.0-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so')
        .replace_needed('libstagefright_foundation.so', 'libstagefright_foundation-v33.so')
        .replace_needed('libui.so', 'libui-v32.so'),

('vendor/lib/mt6985/libmtkcam_stdutils.so',
     'vendor/lib/hw/mt6985/android.hardware.camera.provider@2.6-impl-mediatek.so'): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),

('vendor/lib/libcodec2_mtk_vdec.so', 'vendor/lib/libcodec2_mtk_venc.so', 'vendor/lib/libcodec2_vpp_dolby_plugin.so'): blob_fixup()
        .replace_needed('libcodec2_soft_common.so', 'libcodec2_soft_common-v31.so')
        .replace_needed('libcodec2_vndk.so', 'libcodec2_vndk-v31.so'),

    'vendor/lib64/libMiPhotoFilter.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_isSupported')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
}  # fmt: skip

module = ExtractUtilsModule(
    'corot',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
