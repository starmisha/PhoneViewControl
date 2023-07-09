package com.example.testresiever;


import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.view.LayoutInflater;
import android.view.ViewGroup;

public class MainActivity extends Activity {
    CallReciever reciever = new CallReciever();
    String state = reciever.getState();
    @Override
    public void onCreate(Bundle savedInstanceState) {


        super.onCreate(savedInstanceState);
    }

    @Override
    protected void onStart() {
        super.onStart();
        IntentFilter filter = new IntentFilter(TelephonyManager.EXTRA_STATE_RINGING);
        registerReceiver(reciever, filter);
        state = reciever.getState();
        System.out.println(state);

        if (state!=null && state.equals(TelephonyManager.EXTRA_STATE_RINGING)) {
            Intent i=new Intent(this, phone_services.class);

                startService(i);

        }



    }


    @Override
    protected void onStop() {
        super.onStop();
        unregisterReceiver(reciever);
    }}



//    private void openCamera() {
//        Intent intent = new Intent( "android.media.action.VIDEO_CAPTURE");
//        startActivity(intent);
//    }}
