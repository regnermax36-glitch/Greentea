package com.maxregner.maps.ui.components
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import org.maplibre.android.maps.MapView
import org.maplibre.android.maps.Style
@Composable
fun MapLibreView(modifier: Modifier = Modifier) {
    AndroidView(modifier = modifier, factory = { context ->
        MapView(context).apply {
            getMapAsync { map -> map.setStyle(Style.Builder().fromUri("asset://maxregner_style.json")) }
        }
    })
}
