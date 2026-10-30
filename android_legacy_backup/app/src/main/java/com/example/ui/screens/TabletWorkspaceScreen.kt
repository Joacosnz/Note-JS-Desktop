package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.LibraryBooks
import androidx.compose.material.icons.filled.Brush
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.Checklist
import androidx.compose.material.icons.filled.EditNote
import androidx.compose.material.icons.filled.Folder
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.FullscreenExit
import androidx.compose.material.icons.filled.Tag
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.VerticalDivider
import androidx.compose.material3.windowsizeclass.WindowSizeClass
import androidx.compose.material3.windowsizeclass.WindowWidthSizeClass
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.example.model.NoteType
import com.example.ui.components.NavigationDestination
import com.example.ui.components.NoteJsNavigationRail
import com.example.ui.theme.NoteJsAmber
import com.example.ui.theme.NoteJsAmberDark
import com.example.ui.theme.isAppInDarkTheme
import com.example.ui.utils.rememberWindowSizeClass
import com.example.viewmodel.NavTab
import com.example.viewmodel.NotesViewModel
import com.example.viewmodel.Screen

/**
 * Adaptive NavigationRail + Master-Detail layout for larger screens (Tablets and Desktops)
 * powered by [WindowSizeClass] ([WindowWidthSizeClass.Medium] and [WindowWidthSizeClass.Expanded]).
 */
@Composable
fun TabletWorkspaceScreen(
    viewModel: NotesViewModel,
    windowSizeClass: WindowSizeClass = rememberWindowSizeClass(),
    pendingOpenReminderId: Long = 0L,
    modifier: Modifier = Modifier
) {
    val isExpandedScreen = windowSizeClass.widthSizeClass == WindowWidthSizeClass.Expanded
    val isDark = isAppInDarkTheme()
    val amber = if (isDark) NoteJsAmberDark else NoteJsAmber

    if (isExpandedScreen) {
        DesktopMainScaffold(
            viewModel = viewModel,
            modifier = modifier
        )
        return
    }

    val currentScreen by viewModel.currentScreen.collectAsStateWithLifecycle()
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    var areSidePanelsVisible by rememberSaveable { mutableStateOf(true) }
    var isDetailFullscreen by rememberSaveable { mutableStateOf(false) }

    val drawerBg = if (isDark) Color(0xFF18191D) else Color(0xFFF8F9FA)
    val dividerColor = if (isDark) Color(0xFF2A2B30) else Color(0xFFE2E4E9)

    val selectedDestination = when {
        currentScreen is Screen.Reminders || uiState.activeTab == NavTab.REMINDERS -> NavigationDestination.REMINDERS
        currentScreen is Screen.Folders -> NavigationDestination.FOLDERS
        currentScreen is Screen.PdfLibrary || currentScreen is Screen.PdfViewer -> NavigationDestination.PDF_LIBRARY
        currentScreen is Screen.Settings -> NavigationDestination.SETTINGS
        uiState.activeTab == NavTab.ARCHIVED -> NavigationDestination.ARCHIVED
        uiState.activeTab == NavTab.TRASH -> NavigationDestination.TRASH
        else -> NavigationDestination.NOTES
    }

    Row(
        modifier = modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .testTag("tablet_workspace_screen")
    ) {
        // 1. Material 3 NavigationRail for Medium (600dp+) and Expanded (840dp+) WindowSizeClass
        NoteJsNavigationRail(
            selectedDestination = selectedDestination,
            onSelectDestination = { destination ->
                when (destination) {
                    NavigationDestination.NOTES -> {
                        viewModel.setActiveTab(NavTab.NOTES)
                        viewModel.selectFolder(null)
                        viewModel.selectTag(null)
                        if (currentScreen !is Screen.Home && currentScreen !is Screen.Editor) {
                            viewModel.navigateTo(Screen.Home)
                        }
                    }
                    NavigationDestination.REMINDERS -> {
                        viewModel.navigateTo(Screen.Reminders())
                    }
                    NavigationDestination.FOLDERS -> {
                        viewModel.navigateTo(Screen.Folders)
                    }
                    NavigationDestination.PDF_LIBRARY -> {
                        viewModel.navigateTo(Screen.PdfLibrary)
                    }
                    NavigationDestination.ARCHIVED -> {
                        viewModel.setActiveTab(NavTab.ARCHIVED)
                        viewModel.navigateTo(Screen.Home)
                    }
                    NavigationDestination.TRASH -> {
                        viewModel.setActiveTab(NavTab.TRASH)
                        viewModel.navigateTo(Screen.Home)
                    }
                    NavigationDestination.SETTINGS -> {
                        viewModel.navigateTo(Screen.Settings)
                    }
                }
            },
            onNewNote = {
                viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
            },
            onVoiceNote = {
                viewModel.navigateTo(Screen.Editor(noteId = 0L, openVoiceDictation = true))
            },
            onReadPdf = {
                viewModel.navigateTo(Screen.PdfLibrary)
            },
            onScanDocument = {
                viewModel.navigateTo(Screen.Editor(noteId = 0L, openDocumentScanner = true))
            },
            onNewReminder = {
                viewModel.navigateTo(
                    Screen.Reminders(
                        initialCreateNewReminder = true,
                        triggerTimestamp = System.currentTimeMillis()
                    )
                )
            },
            notesCount = uiState.allActiveNotesCount,
            remindersCount = uiState.remindersCount,
            isDrawerExpanded = areSidePanelsVisible,
            showDrawerToggle = true,
            onToggleDrawer = { areSidePanelsVisible = !areSidePanelsVisible }
        )

        VerticalDivider(color = dividerColor, thickness = 1.dp)

        // Secondary Folders & Tags Panel toggled together with the Notes List from the 3-bars button
        AnimatedVisibility(visible = areSidePanelsVisible) {
            Row(modifier = Modifier.fillMaxHeight()) {
                Surface(
                    color = drawerBg,
                    modifier = Modifier
                        .fillMaxHeight()
                        .width(210.dp)
                        .testTag("tablet_secondary_folders_drawer")
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .statusBarsPadding()
                            .padding(12.dp)
                            .verticalScroll(rememberScrollState()),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Text(
                            text = "CARPETAS",
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Bold,
                                fontSize = 11.sp,
                                letterSpacing = 0.8.sp
                            ),
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )

                        DrawerFilterRow(
                            icon = Icons.Default.Folder,
                            label = "Todas las notas",
                            badgeCount = uiState.allActiveNotesCount,
                            isSelected = uiState.selectedFolder == null && uiState.selectedTag == null,
                            accentColor = amber,
                            onClick = {
                                viewModel.setActiveTab(NavTab.NOTES)
                                viewModel.selectFolder(null)
                                viewModel.selectTag(null)
                            }
                        )

                        val customFolders = uiState.availableFolders.filter {
                            !it.equals("Notas", ignoreCase = true) && !it.equals("Todas", ignoreCase = true)
                        }
                        customFolders.forEach { folderName ->
                            DrawerFilterRow(
                                icon = Icons.Default.Folder,
                                label = folderName,
                                badgeCount = uiState.folderNoteCounts[folderName] ?: 0,
                                isSelected = uiState.selectedFolder == folderName,
                                accentColor = amber,
                                onClick = {
                                    viewModel.setActiveTab(NavTab.NOTES)
                                    viewModel.selectFolder(folderName)
                                    if (currentScreen !is Screen.Home && currentScreen !is Screen.Editor) {
                                        viewModel.navigateTo(Screen.Home)
                                    }
                                }
                            )
                        }

                        val userTags = uiState.availableTags.filter { it != "Todas" }
                        if (userTags.isNotEmpty()) {
                            Spacer(modifier = Modifier.height(8.dp))
                            HorizontalDivider(color = dividerColor)
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "ETIQUETAS",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    fontSize = 11.sp,
                                    letterSpacing = 0.8.sp
                                ),
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                            )
                            userTags.forEach { tag ->
                                DrawerFilterRow(
                                    icon = Icons.Default.Tag,
                                    label = if (tag.startsWith("#")) tag else "#$tag",
                                    isSelected = uiState.selectedTag == tag,
                                    accentColor = amber,
                                    onClick = {
                                        viewModel.setActiveTab(NavTab.NOTES)
                                        viewModel.selectTag(tag)
                                        if (currentScreen !is Screen.Home && currentScreen !is Screen.Editor) {
                                            viewModel.navigateTo(Screen.Home)
                                        }
                                    }
                                )
                            }
                        }
                    }
                }
                VerticalDivider(color = dividerColor, thickness = 1.dp)
            }
        }

        // 2. Main Content Area (Split Master-Detail on Expanded screens, or adaptive two-pane)
        Box(modifier = Modifier.weight(1f).fillMaxHeight()) {
            when (val screen = currentScreen) {
                is Screen.Home, is Screen.Editor, is Screen.Drawing -> {
                    val isEditingNote = screen is Screen.Editor || screen is Screen.Drawing
                    // The 3-bars button hides/shows both the folders panel and the all-notes list pane
                    val showListPane = areSidePanelsVisible && (!isDetailFullscreen || !isEditingNote)

                    Row(modifier = Modifier.fillMaxSize()) {
                        AnimatedVisibility(visible = showListPane) {
                            Row(modifier = Modifier.fillMaxHeight()) {
                                Box(
                                    modifier = Modifier
                                        .width(if (isExpandedScreen) 400.dp else 320.dp)
                                        .fillMaxHeight()
                                ) {
                                    HomeScreen(viewModel = viewModel)
                                }
                                VerticalDivider(color = dividerColor, thickness = 1.dp)
                            }
                        }

                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .fillMaxHeight()
                        ) {
                            when (screen) {
                                is Screen.Editor -> {
                                    Box(modifier = Modifier.fillMaxSize()) {
                                        NoteEditorScreen(
                                            noteId = screen.noteId,
                                            initialType = screen.initialType,
                                            initialOpenVoiceDictation = screen.openVoiceDictation,
                                            initialOpenDocumentScanner = screen.openDocumentScanner,
                                            initialSharedText = screen.initialSharedText,
                                            initialSharedTitle = screen.initialSharedTitle,
                                            viewModel = viewModel
                                        )
                                        Surface(
                                            shape = CircleShape,
                                            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.85f),
                                            modifier = Modifier
                                                .align(Alignment.TopEnd)
                                                .statusBarsPadding()
                                                .padding(top = 8.dp, end = 56.dp)
                                        ) {
                                            IconButton(
                                                onClick = { isDetailFullscreen = !isDetailFullscreen },
                                                modifier = Modifier.size(36.dp)
                                            ) {
                                                Icon(
                                                    imageVector = if (isDetailFullscreen) Icons.Default.FullscreenExit else Icons.Default.Fullscreen,
                                                    contentDescription = if (isDetailFullscreen) "Mostrar lista lateral" else "Expandir editor",
                                                    tint = amber,
                                                    modifier = Modifier.size(20.dp)
                                                )
                                            }
                                        }
                                    }
                                }
                                is Screen.Drawing -> {
                                    DrawingScreen(
                                        noteId = screen.noteId,
                                        viewModel = viewModel
                                    )
                                }
                                else -> {
                                    TabletEmptyDetailPlaceholder(
                                        accentColor = amber,
                                        onNewTextNote = {
                                            viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.TEXT))
                                        },
                                        onNewChecklist = {
                                            viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.CHECKLIST))
                                        },
                                        onNewDrawing = {
                                            viewModel.navigateTo(Screen.Drawing(noteId = 0L))
                                        },
                                        onNewMathNote = {
                                            viewModel.navigateTo(Screen.Editor(noteId = 0L, initialType = NoteType.MATH))
                                        },
                                        onOpenFirstNote = {
                                            val firstNote = uiState.activeNotes.firstOrNull { !it.isLocked }
                                            if (firstNote != null) {
                                                viewModel.navigateTo(
                                                    Screen.Editor(
                                                        noteId = firstNote.id,
                                                        initialType = runCatching { NoteType.valueOf(firstNote.noteType) }.getOrDefault(NoteType.TEXT)
                                                    )
                                                )
                                            }
                                        },
                                        hasAvailableNotes = uiState.activeNotes.any { !it.isLocked }
                                    )
                                }
                            }
                        }
                    }
                }

                is Screen.Folders -> {
                    FoldersScreen(viewModel = viewModel)
                }

                is Screen.PdfViewer -> {
                    PdfViewerScreen(
                        noteId = screen.noteId,
                        pdfPath = screen.pdfPath,
                        viewModel = viewModel
                    )
                }

                is Screen.PdfLibrary -> {
                    PdfLibraryScreen(viewModel = viewModel)
                }

                is Screen.Settings -> {
                    SettingsScreen(viewModel = viewModel)
                }

                is Screen.Reminders -> {
                    RemindersScreen(
                        viewModel = viewModel,
                        initialOpenReminderId = if (screen.initialOpenReminderId != 0L) screen.initialOpenReminderId else pendingOpenReminderId,
                        initialCreateNewReminder = screen.initialCreateNewReminder || (pendingOpenReminderId == -2L),
                        creationTriggerTimestamp = screen.triggerTimestamp
                    )
                }
            }
        }
    }
}

@Composable
private fun DrawerFilterRow(
    icon: ImageVector,
    label: String,
    badgeCount: Int = 0,
    isSelected: Boolean,
    accentColor: Color,
    onClick: () -> Unit
) {
    val bgColor = if (isSelected) accentColor.copy(alpha = 0.16f) else Color.Transparent
    val contentColor = if (isSelected) accentColor else MaterialTheme.colorScheme.onSurfaceVariant

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(10.dp))
            .background(bgColor)
            .clickable(onClick = onClick)
            .padding(horizontal = 10.dp, vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = icon,
            contentDescription = label,
            tint = accentColor,
            modifier = Modifier.size(18.dp)
        )
        Spacer(modifier = Modifier.width(10.dp))
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium.copy(
                fontWeight = if (isSelected) FontWeight.SemiBold else FontWeight.Normal,
                fontSize = 13.5.sp
            ),
            color = if (isSelected) MaterialTheme.colorScheme.onSurface else contentColor,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.weight(1f)
        )
        if (badgeCount > 0) {
            Text(
                text = badgeCount.toString(),
                style = MaterialTheme.typography.labelSmall.copy(
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 11.5.sp
                ),
                color = contentColor
            )
        }
    }
}

@Composable
private fun TabletEmptyDetailPlaceholder(
    accentColor: Color,
    onNewTextNote: () -> Unit,
    onNewChecklist: () -> Unit,
    onNewDrawing: () -> Unit,
    onNewMathNote: () -> Unit,
    onOpenFirstNote: () -> Unit,
    hasAvailableNotes: Boolean
) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(28.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier.width(380.dp)
        ) {
            Box(
                modifier = Modifier
                    .size(68.dp)
                    .clip(RoundedCornerShape(18.dp))
                    .background(accentColor.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = Icons.Default.EditNote,
                    contentDescription = null,
                    tint = accentColor,
                    modifier = Modifier.size(36.dp)
                )
            }

            Spacer(modifier = Modifier.height(18.dp))

            Text(
                text = "Vista Dividida Activa",
                style = MaterialTheme.typography.headlineSmall.copy(
                    fontWeight = FontWeight.Bold,
                    fontSize = 21.sp
                ),
                color = MaterialTheme.colorScheme.onSurface,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = "Selecciona una nota de la lista o crea un documento nuevo usando el NavigationRail lateral.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                textAlign = TextAlign.Center
            )

            Spacer(modifier = Modifier.height(22.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                OutlinedButton(
                    onClick = onNewTextNote,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Icon(Icons.AutoMirrored.Filled.LibraryBooks, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Texto", maxLines = 1)
                }

                OutlinedButton(
                    onClick = onNewChecklist,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Icon(Icons.Default.Checklist, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Checklist", maxLines = 1)
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                OutlinedButton(
                    onClick = onNewMathNote,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Icon(Icons.Default.Calculate, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("KaTeX / Math", maxLines = 1)
                }

                OutlinedButton(
                    onClick = onNewDrawing,
                    shape = RoundedCornerShape(12.dp),
                    modifier = Modifier.weight(1f).height(44.dp)
                ) {
                    Icon(Icons.Default.Brush, contentDescription = null, modifier = Modifier.size(18.dp))
                    Spacer(modifier = Modifier.width(6.dp))
                    Text("Dibujo", maxLines = 1)
                }
            }

            if (hasAvailableNotes) {
                Spacer(modifier = Modifier.height(14.dp))
                Button(
                    onClick = onOpenFirstNote,
                    shape = RoundedCornerShape(12.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = accentColor,
                        contentColor = Color.Black
                    ),
                    modifier = Modifier.fillMaxWidth().height(44.dp)
                ) {
                    Text("Abrir nota más reciente", fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}
