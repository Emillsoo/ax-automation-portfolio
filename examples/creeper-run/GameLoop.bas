Attribute VB_Name = "GameLoop"
Option Explicit

' Public, minimal reconstruction of a PowerPoint VBA game loop.
' It does not include third-party images or the original presentation.

Private Const MAX_OBJECTS As Long = 24
Private objects As Collection
Private score As Long
Private lives As Long
Private running As Boolean

Public Sub StartDemoGame()
    Set objects = New Collection
    score = 0
    lives = 3
    running = True
    ScheduleNextTick
End Sub

Public Sub StopDemoGame()
    running = False
    RemoveAllObjects
End Sub

Public Sub Tick()
    If Not running Then Exit Sub

    MovePlayerFromKeyState
    MoveObjects
    RemoveExpiredObjects

    If objects.Count < MAX_OBJECTS Then
        SpawnSyntheticObject
    End If

    ResolveCollisions
    score = score + 1

    If lives <= 0 Then
        StopDemoGame
    Else
        ScheduleNextTick
    End If
End Sub

Private Sub MovePlayerFromKeyState()
    ' Presentation-specific key polling is intentionally omitted.
End Sub

Private Sub MoveObjects()
    ' Move only shapes owned by this game instance.
End Sub

Private Sub RemoveExpiredObjects()
    ' Delete off-screen objects so shapes do not accumulate indefinitely.
End Sub

Private Sub SpawnSyntheticObject()
    ' Add a simple geometric shape, not a copyrighted game asset.
End Sub

Private Sub ResolveCollisions()
    ' Apply one hit per object, then remove that object.
End Sub

Private Sub ScheduleNextTick()
    ' The original presentation schedules the next frame safely.
End Sub

Private Sub RemoveAllObjects()
    Set objects = New Collection
End Sub
