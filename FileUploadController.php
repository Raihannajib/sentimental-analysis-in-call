<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Controllers\HelperController;

class FileUploadController extends Controller
{
    //
    public function fileUpload() {
        return view('admin');
    }

    public function fileUploadPost(Request $request) {
        
        $request->validate([
            'file' => 'required|mimes:pdf,png,jpg,jpeg|max:2048',
        ]);

        $file_name = pathinfo($request->file->getClientOriginalName(), PATHINFO_FILENAME);


        $filename = strtoupper(trim( $file_name)).'-'.date('Y-m-d').'.'.$request->file->extension();
        $request->file->move(public_path('uploads'),$filename);
        return back()
                ->with('success','You have successfully upload file.')
                ->with('file',$filename);
    }

    public function show_files() {
            $filenames = HelperController::parse();
            // return view('files',['filenamepdf' => $filenames[0],'filenameimg' => $filenames[1]]);
            return response()->json([
                'filenames'  => $filenames,

            ]);

        // dd($filenames);
    }

    public function showfiles() {
        return view('files');
    }




    // public function deleteFile()
    // {  
    // if(\File::exists(public_path('upload/avtar.png'))){
    //     \File::delete(public_path('upload/avtar.png'));
    // }else{
    //     dd('File does not exists.');
    // }
    // } 

}
