package com.example.testresiever;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.graphics.PixelFormat;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.Console;



public class CallReciever extends BroadcastReceiver {
    private static boolean incomingCall = false;
    private static WindowManager windowManager;
    private static ViewGroup windowLayout;
    String state,number,message;
    String  TAG = "stateChanged";

    @Override
    public void onReceive(Context context, Intent intent) {
        state = intent.getStringExtra(TelephonyManager.EXTRA_STATE);
        if(state.equals(TelephonyManager.CALL_STATE_RINGING)){
            number = intent.getStringExtra(TelephonyManager.EXTRA_INCOMING_NUMBER);
//            Log.debug("Show window: " + number);

            message = "phone is ringing";
            getState();
            showWindow(context, number);//добавили
            System.out.println(state);



        }
        if ((state.equals(TelephonyManager.EXTRA_STATE_OFFHOOK))){
//            Log.debug("Close window.");
            closeWindow();//добавили
        }
        if (state.equals(TelephonyManager.EXTRA_STATE_IDLE)){
            message += "phone is idled";
            Toast.makeText(context, "Idled", Toast.LENGTH_SHORT).show();


        }


        }

    public String getState() {
        return this.state;
    }


   private void showWindow(Context context, String phone) {
           windowManager = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
           LayoutInflater layoutInflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);

           WindowManager.LayoutParams params = new WindowManager.LayoutParams(
           WindowManager.LayoutParams.MATCH_PARENT,
           WindowManager.LayoutParams.WRAP_CONTENT,
           WindowManager.LayoutParams.TYPE_SYSTEM_ALERT,
           WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL,
           PixelFormat.TRANSLUCENT);
           params.gravity = Gravity.TOP;

           windowLayout = (ViewGroup) layoutInflater.inflate(R.layout.pop_layout, null);

           TextView textViewNumber=(TextView) windowLayout.findViewById(R.id.textViewNumber);

           textViewNumber.setText(phone);
           Button buttonClose = windowLayout.findViewById(R.id.buttonClose);
           buttonClose.setOnClickListener(new View.OnClickListener() {
@Override
public void onClick(View v) {
        closeWindow();
        }
        });

        windowManager.addView(windowLayout, params);
        }

private void closeWindow() {
        if (windowLayout !=null){
        windowManager.removeView(windowLayout);
        windowLayout =null;
        }
        }
        }









