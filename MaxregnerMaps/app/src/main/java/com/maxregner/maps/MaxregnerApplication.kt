package com.maxregner.maps
import android.app.Application
import org.maplibre.android.MapLibre
class MaxregnerApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        MapLibre.getInstance(this)
    }
}
