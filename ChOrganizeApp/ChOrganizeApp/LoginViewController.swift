//
//  LoginViewController.swift
//  ChOrganizeApp
//
//  Created by Hana on 11/8/17.
//  Copyright © 2017 Pusheen Code. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {
    let BASE_URL = "http://shea3100.pythonanywhere.com"
    let VALIDATE_USER_URL = "/api/user/get"
    
    @IBOutlet weak var emailField: UITextField!
    @IBOutlet weak var passwordField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }
    
    private func moveToToDo() {
        print("in move to")
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let TabBarVC = storyboard.instantiateViewController(withIdentifier: "TabBarController") as! UITabBarController
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        appDelegate.window?.rootViewController = TabBarVC
    }
    
    private func emptyLoginParamsAlert() {
        let alert = UIAlertController(
            title: "Error",
            message: "Please enter a valid email and password to Login",
            preferredStyle: .alert)
        
        alert.addAction(UIAlertAction(title: NSLocalizedString("OK", comment: "Default action"), style: .`default`, handler: nil))
        self.present(alert, animated: true, completion: nil)
    }
    
    @IBAction func userLogin(_ sender: Any) {
        // TODO: validate fields
        // TODO: make password field starred out
        
        // check required fields are entered
        if emailField.text == "" || passwordField.text == "" {
            // popup alert
            emptyLoginParamsAlert()
        }
        else {
            // try to validate user
            validateUserRequest()
        }
    }
    
    private func validateUserRequest() {
        let emailInput = emailField.text
        let passwordInput = passwordField.text
        print("user inputs:")
        print(emailInput)
        print(passwordInput)
        
        // setup GET request for VALIDATE_USER_URL
        var components = URLComponents(string: BASE_URL + VALIDATE_USER_URL)!
        components.queryItems = [
            URLQueryItem(name: "email", value: emailInput),
            URLQueryItem(name: "password", value: passwordInput)
        ]
        var request = URLRequest(url: components.url!)
        request.httpMethod = "GET"
        
        print("staritng request")
        let task = URLSession.shared.dataTask(with: request){ data, response, error in
            guard let data = data, error == nil else {
                print("error=\(error)")
                return
            }
            
            if let httpStatus = response as? HTTPURLResponse, httpStatus.statusCode != 200 {
                print("statusCode should be 200, but is \(httpStatus.statusCode)")
                print("response = \(response)")
                // TODO: popup alert based on response
            }
            
            // success
            let responseString = String(data: data, encoding: .utf8)
            print("responseString = \(responseString)")
            
            DispatchQueue.main.async {
                self.moveToToDo()
            }
        }
        task.resume()
        print("finished")
    }
}
