package com.example.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Archive
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.DocumentScanner
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.MenuOpen
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Notifications
import androidx.compose.material.icons.filled.PictureAsPdf
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.Badge
import androidx.compose.material3.BadgedBox
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.FloatingActionButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationRail
import androidx.compose.material3.NavigationRailItem
import androidx.compose.material3.NavigationRailItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.ui.theme.NoteJsAmber
import com.example.ui.theme.NoteJsAmberDark
import com.example.ui.theme.isAppInDarkTheme

enum class NavigationDestination {
    NOTES,
    REMINDERS,
    FOLDERS,
    PDF_LIBRARY,
    ARCHIVED,
    TRASH,
    SETTINGS
}

/**
 * Material 3 [NavigationRail] component for larger screens (Tablets and Desktops)
 * detected via [androidx.compose.material3.windowsizeclass.WindowSizeClass].
 */
@Composable
fun NoteJsNavigationRail(
    selectedDestination: NavigationDestination,
    onSelectDestination: (NavigationDestination) -> Unit,
    onNewNote: () -> Unit,
    onVoiceNote: () -> Unit = {},
    onReadPdf: () -> Unit = {},
    onScanDocument: () -> Unit = {},
    onNewReminder: () -> Unit = {},
    notesCount: Int = 0,
    remindersCount: Int = 0,
    isDrawerExpanded: Boolean = false,
    showDrawerToggle: Boolean = true,
    onToggleDrawer: () -> Unit = {},
    modifier: Modifier = Modifier
) {
    val isDark = isAppInDarkTheme()
    val amber = if (isDark) NoteJsAmberDark else NoteJsAmber
    val railContainerColor = if (isDark) Color(0xFF141518) else Color(0xFFF3F4F6)
    var showCreateMenu by remember { mutableStateOf(false) }

    val itemColors = NavigationRailItemDefaults.colors(
        selectedIconColor = Color.Black,
        selectedTextColor = amber,
        indicatorColor = amber,
        unselectedIconColor = MaterialTheme.colorScheme.onSurfaceVariant,
        unselectedTextColor = MaterialTheme.colorScheme.onSurfaceVariant
    )

    NavigationRail(
        modifier = modifier
            .fillMaxHeight()
            .testTag("notejs_navigation_rail"),
        containerColor = railContainerColor,
        contentColor = MaterialTheme.colorScheme.onSurface,
        header = {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(8.dp),
                modifier = Modifier.padding(top = 8.dp)
            ) {
                if (showDrawerToggle) {
                    IconButton(
                        onClick = onToggleDrawer,
                        modifier = Modifier.testTag("rail_toggle_drawer_button")
                    ) {
                        Icon(
                            imageVector = if (isDrawerExpanded) Icons.Default.MenuOpen else Icons.Default.Menu,
                            contentDescription = if (isDrawerExpanded) "Ocultar panel de carpetas" else "Mostrar panel de carpetas",
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                }

                Box {
                    FloatingActionButton(
                        onClick = onNewNote,
                        shape = RoundedCornerShape(16.dp),
                        containerColor = amber,
                        contentColor = Color.Black,
                        elevation = FloatingActionButtonDefaults.elevation(defaultElevation = 2.dp),
                        modifier = Modifier
                            .size(52.dp)
                            .testTag("rail_fab_new_note")
                    ) {
                        Icon(
                            imageVector = Icons.Default.Add,
                            contentDescription = "Nueva Nota",
                            modifier = Modifier.size(24.dp)
                        )
                    }

                    DropdownMenu(
                        expanded = showCreateMenu,
                        onDismissRequest = { showCreateMenu = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("Nueva Nota de Texto") },
                            leadingIcon = { Icon(Icons.Default.Add, contentDescription = null) },
                            onClick = {
                                showCreateMenu = false
                                onNewNote()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Nota de Voz") },
                            leadingIcon = { Icon(Icons.Default.Mic, contentDescription = null) },
                            onClick = {
                                showCreateMenu = false
                                onVoiceNote()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Nuevo Recordatorio") },
                            leadingIcon = { Icon(Icons.Default.Notifications, contentDescription = null) },
                            onClick = {
                                showCreateMenu = false
                                onNewReminder()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Leer PDF") },
                            leadingIcon = { Icon(Icons.Default.PictureAsPdf, contentDescription = null) },
                            onClick = {
                                showCreateMenu = false
                                onReadPdf()
                            }
                        )
                        DropdownMenuItem(
                            text = { Text("Escanear Documento") },
                            leadingIcon = { Icon(Icons.Default.DocumentScanner, contentDescription = null) },
                            onClick = {
                                showCreateMenu = false
                                onScanDocument()
                            }
                        )
                    }
                }
            }
        }
    ) {
        Column(
            modifier = Modifier
                .fillMaxHeight()
                .verticalScroll(rememberScrollState())
                .padding(vertical = 8.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.NOTES,
                onClick = { onSelectDestination(NavigationDestination.NOTES) },
                icon = {
                    BadgedBox(
                        badge = {
                            if (notesCount > 0) {
                                Badge(
                                    containerColor = amber.copy(alpha = 0.22f),
                                    contentColor = MaterialTheme.colorScheme.onSurface
                                ) {
                                    Text(notesCount.toString(), fontSize = 10.sp)
                                }
                            }
                        }
                    ) {
                        Icon(
                            imageVector = Icons.Default.Home,
                            contentDescription = "Notas"
                        )
                    }
                },
                label = {
                    Text(
                        text = "Notas",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.NOTES) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_home")
            )

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.REMINDERS,
                onClick = { onSelectDestination(NavigationDestination.REMINDERS) },
                icon = {
                    BadgedBox(
                        badge = {
                            if (remindersCount > 0) {
                                Badge(
                                    containerColor = amber,
                                    contentColor = Color.Black
                                ) {
                                    Text(remindersCount.toString(), fontSize = 10.sp)
                                }
                            }
                        }
                    ) {
                        Icon(
                            imageVector = Icons.Default.Notifications,
                            contentDescription = "Recordatorios"
                        )
                    }
                },
                label = {
                    Text(
                        text = "Agenda",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.REMINDERS) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_reminders")
            )

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.FOLDERS,
                onClick = { onSelectDestination(NavigationDestination.FOLDERS) },
                icon = {
                    Icon(
                        imageVector = Icons.Default.Folder,
                        contentDescription = "Carpetas"
                    )
                },
                label = {
                    Text(
                        text = "Carpetas",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.FOLDERS) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_folders")
            )

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.PDF_LIBRARY,
                onClick = { onSelectDestination(NavigationDestination.PDF_LIBRARY) },
                icon = {
                    Icon(
                        imageVector = Icons.Default.PictureAsPdf,
                        contentDescription = "Biblioteca PDF"
                    )
                },
                label = {
                    Text(
                        text = "PDFs",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.PDF_LIBRARY) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_pdf")
            )

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.ARCHIVED,
                onClick = { onSelectDestination(NavigationDestination.ARCHIVED) },
                icon = {
                    Icon(
                        imageVector = Icons.Default.Archive,
                        contentDescription = "Archivadas"
                    )
                },
                label = {
                    Text(
                        text = "Archivo",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.ARCHIVED) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_archived")
            )

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.TRASH,
                onClick = { onSelectDestination(NavigationDestination.TRASH) },
                icon = {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Papelera"
                    )
                },
                label = {
                    Text(
                        text = "Papelera",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.TRASH) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_trash")
            )

            Spacer(modifier = Modifier.weight(1f))

            HorizontalDivider(modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp))

            NavigationRailItem(
                selected = selectedDestination == NavigationDestination.SETTINGS,
                onClick = { onSelectDestination(NavigationDestination.SETTINGS) },
                icon = {
                    Icon(
                        imageVector = Icons.Default.Settings,
                        contentDescription = "Ajustes"
                    )
                },
                label = {
                    Text(
                        text = "Ajustes",
                        fontSize = 11.sp,
                        fontWeight = if (selectedDestination == NavigationDestination.SETTINGS) FontWeight.Bold else FontWeight.Medium
                    )
                },
                colors = itemColors,
                modifier = Modifier.testTag("rail_nav_settings")
            )

            Spacer(modifier = Modifier.height(8.dp))
        }
    }
}
