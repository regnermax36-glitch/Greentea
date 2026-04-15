package com.maxregner.maps.ui.components
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import org.maplibre.android.maps.MapView
import org.maplibre.android.maps.Style
@Composable
fun MapLibreView(mapView: MapView, modifier: Modifier = Modifier) {
    AndroidView(modifier = modifier, factory = { mapView }) { view ->
        view.getMapAsync { map ->
            if (map.style == null) {
                map.setStyle(Style.Builder().fromUri("asset://maxregner_style.json"))
            }
        }
    }
}
