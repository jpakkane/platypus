package io.github.jpakkane.platypus

import android.os.Bundle
import androidx.activity.ComponentActivity
import android.widget.Button
import android.widget.TextView
import io.github.jpakkane.platypus.ui.theme.PlatypusTheme

class MainActivity : ComponentActivity() {

    var actionButton: Button? = null
    var textEntry: TextView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        System.loadLibrary("platypus")
        setContentView(R.layout.activity_main)
        actionButton = findViewById(R.id.button2)
        textEntry = findViewById(R.id.sample_text)
        actionButton!!.setOnClickListener { buttonClicked() }
    }

    fun buttonClicked() {
        val x: Int = platypus_hello()
        textEntry!!.text = getString(R.string.got_value, x)
    }

    external fun platypus_hello(): Int
}
