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

#include<platypus.h>
#include<gtk/gtk.h>

struct App {
    GtkBuilder *builder;
    GtkWindow *main_window;
    GtkButton *call_button;
    GtkButton *quit_button;
    GtkLabel *status_label;
};

void call_callback(GtkButton *b, gpointer data) {
    struct App *a = (struct App*)(data);
    (void)b;
    int value = platypus_hello();
    char buf[1024];
    snprintf(buf, 1024, "Library returned value %d.", value);
    gtk_label_set_text(a->status_label, buf);
}

void build_gui(struct App *a) {
    a->builder = gtk_builder_new_from_file(GLADE_FILE);
    //a->builder = gtk_builder_new_from_file("../gtk/platygui.glade");
    a->main_window = GTK_WINDOW(gtk_builder_get_object(a->builder, "main_window"));
    a->call_button = GTK_BUTTON(gtk_builder_get_object(a->builder, "call_button"));
    a->quit_button = GTK_BUTTON(gtk_builder_get_object(a->builder, "quit_button"));
    a->status_label = GTK_LABEL(gtk_builder_get_object(a->builder, "status_label"));

    g_signal_connect(GTK_WIDGET(a->main_window), "destroy", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(GTK_WIDGET(a->quit_button), "clicked", G_CALLBACK(gtk_main_quit), NULL);
    g_signal_connect(GTK_WIDGET(a->call_button), "clicked", G_CALLBACK(call_callback), a);
    gtk_widget_show_all(GTK_WIDGET(a->main_window));
}

int main(int argc, char **argv) {
    struct App a;
    gtk_init(&argc, &argv);
    build_gui(&a);
    gtk_main();
    g_object_unref(G_OBJECT(a.builder));
    g_object_unref(G_OBJECT(a.main_window));
    return 0;
}

