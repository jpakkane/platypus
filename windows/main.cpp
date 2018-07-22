/*
 * Copyright 2018 Jussi Pakkanen
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include<windows.h>
#include<string>

#define ID_CALL_LIB 55

HWND hwndlabel, hwndbutton;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE, PSTR, int iCmdShow) {
    static TCHAR name[] = TEXT("Platypus");
    RECT rcClient;  // dimensions of client area
    HWND hwnd;
    MSG msg;
    WNDCLASS wndclass;

//    InitCommonControls();

    wndclass.style = CS_HREDRAW | CS_VREDRAW;
    wndclass.lpfnWndProc = WndProc;
    wndclass.cbClsExtra = 0;
    wndclass.cbWndExtra = 0;
    wndclass.hInstance = hInstance;
    wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
    wndclass.hbrBackground = (HBRUSH) GetStockObject(WHITE_BRUSH);
    wndclass.lpszMenuName = NULL;
    wndclass.lpszClassName = name;

    if(!RegisterClass(&wndclass)) {
      MessageBox(NULL, TEXT("Could not initialize wndclass"), name, MB_ICONERROR);
      return 0;
    }

    hwnd = CreateWindow(name,
                        TEXT("Platypus"),
                        WS_OVERLAPPEDWINDOW,
                        CW_USEDEFAULT,
                        CW_USEDEFAULT,
                        640,
                        240,
                        NULL,
                        NULL,
                        hInstance,
                        NULL);

    GetClientRect(hwnd, &rcClient);

    hwndlabel = CreateWindow("Static",
        "Library has not been called yet",
        WS_CHILD | SS_SUNKEN | SS_CENTER | SS_CENTERIMAGE,
        0,
        20,
        640,
        50,
        hwnd,
        NULL,
        hInstance,
        NULL);

    hwndbutton = CreateWindow("Button",
                              "Call library",
                              WS_CHILD,
                              10,
                              100,
                              600,
                              90,
                              hwnd,
                              (HMENU)ID_CALL_LIB,
                              hInstance,
                              NULL);

    ShowWindow(hwndbutton, iCmdShow);
    UpdateWindow(hwndbutton);
    ShowWindow(hwndlabel, iCmdShow);
    UpdateWindow(hwndlabel);
    ShowWindow(hwnd, iCmdShow);
    UpdateWindow(hwnd);
    while(GetMessage(&msg, NULL, 0, 0)) {
      TranslateMessage(&msg);
      DispatchMessage(&msg);
    }
    return msg.wParam;
}

LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_DESTROY: {
        PostQuitMessage(0);
        return 0;
    }

    case WM_COMMAND: {
        if (LOWORD(wParam) == ID_CALL_LIB) {
            const int result = 42;
            std::string msg("Library returned value: ");
            msg += std::to_string(result);
            msg += ".";
            SetWindowText(hwndlabel, msg.c_str());
        }
    }
    }
  return DefWindowProc(hwnd, message, wParam, lParam);
}
