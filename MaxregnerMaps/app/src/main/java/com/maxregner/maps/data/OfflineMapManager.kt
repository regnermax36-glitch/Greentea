package com.maxregner.maps.data
import android.content.Context
import org.maplibre.android.offline.OfflineManager
import org.maplibre.android.offline.OfflineRegion
import org.maplibre.android.offline.OfflineTilePyramidRegionDefinition
import org.maplibre.android.geometry.LatLngBounds
import org.maplibre.android.geometry.LatLng
import org.json.JSONObject

class OfflineMapManager(private val context: Context) {
    fun downloadGermany() {
        val manager = OfflineManager.getInstance(context)
        val bounds = LatLngBounds.Builder().include(LatLng(55.0, 5.0)).include(LatLng(47.0, 15.0)).build()
        val definition = OfflineTilePyramidRegionDefinition("asset://maxregner_style.json", bounds, 0.0, 10.0, 1.0f)
        val metadata = JSONObject().put("region_name", "Germany").toString().toByteArray()
        manager.createOfflineRegion(definition, metadata, object : OfflineManager.CreateOfflineRegionCallback {
            override fun onCreate(region: OfflineRegion) { region.setDownloadState(OfflineRegion.STATE_ACTIVE) }
            override fun onError(error: String) {}
        })
    }
}
