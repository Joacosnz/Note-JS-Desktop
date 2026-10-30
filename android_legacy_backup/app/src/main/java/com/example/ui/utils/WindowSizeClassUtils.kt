package com.example.ui.utils

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import androidx.compose.material3.windowsizeclass.ExperimentalMaterial3WindowSizeClassApi
import androidx.compose.material3.windowsizeclass.WindowHeightSizeClass
import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.material3.windowsizeclass.calculateWindowSizeClass
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.DpSize
import androidx.compose.ui.unit.dp

/**
 * Calculates the current [WindowSizeClass] using the Activity window metrics when available,
 * and falls back to [LocalConfiguration] screen dimensions in previews or test environments.
 */
@OptIn(ExperimentalMaterial3WindowSizeClassApi::class)
@Composable
fun rememberWindowSizeClass(): WindowSizeClass {
    val context = LocalContext.current
    val configuration = LocalConfiguration.current
    val activity = context.findWindowActivity()
    return if (activity != null) {
        calculateWindowSizeClass(activity = activity)
    } else {
        WindowSizeClass.calculateFromSize(
            DpSize(
                width = configuration.screenWidthDp.dp,
                height = configuration.screenHeightDp.dp
            )
        )
    }
}

/**
 * Returns true when the current [WindowSizeClass] width is [WindowWidthSizeClass.Medium]
 * or [WindowWidthSizeClass.Expanded] (tablets, foldables, and desktops >= 600dp),
 * indicating that a [androidx.compose.material3.NavigationRail] layout should be used
 * instead of a mobile BottomNavigation layout.
 */
val WindowSizeClass.shouldUseNavigationRail: Boolean
    get() = widthSizeClass == WindowWidthSizeClass.Medium ||
        widthSizeClass == WindowWidthSizeClass.Expanded

/**
 * Returns true when the current [WindowSizeClass] width is [WindowWidthSizeClass.Expanded]
 * (large tablets in landscape and desktops >= 840dp).
 */
val WindowSizeClass.isExpandedScreen: Boolean
    get() = widthSizeClass == WindowWidthSizeClass.Expanded

/**
 * Returns true when the current [WindowSizeClass] width is [WindowWidthSizeClass.Compact]
 * (mobile phones < 600dp), indicating a BottomNavigation layout should be used.
 */
val WindowSizeClass.isCompactScreen: Boolean
    get() = widthSizeClass == WindowWidthSizeClass.Compact

val WindowSizeClass.isCompactHeight: Boolean
    get() = heightSizeClass == WindowHeightSizeClass.Compact

private tailrec fun Context.findWindowActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findWindowActivity()
    else -> null
}
